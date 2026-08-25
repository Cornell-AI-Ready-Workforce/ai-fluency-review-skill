#!/usr/bin/env python3
"""Render an AI Fluency Review v0.2 record as standalone HTML."""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

VERSION = "0.2.0"
AREA_ORDER = ["description", "delegation", "discernment", "diligence", "adaptive-flexibility"]
DETAIL_IDS = AREA_ORDER[:4]
EXPECTED_LABELS = {
    "description": ("Brief the task", "Description"),
    "delegation": ("Divide the work", "Delegation"),
    "discernment": ("Check the result", "Discernment"),
    "diligence": ("Finish responsibly", "Diligence"),
    "adaptive-flexibility": ("Learn and adapt", "Adaptive Flexibility"),
}
RATINGS = {
    None: "Not enough evidence",
    1: "Rarely observed",
    2: "Emerging",
    3: "Usually observed",
    4: "Consistent across contexts",
    5: "Consistent and reusable",
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(record: dict) -> dict[str, dict]:
    for key in ("schema_version", "rubric_version", "renderer_version"):
        require(record.get(key) == VERSION, f"{key} must be {VERSION}")
    for key in ("meta", "evidence_inventory", "reliability", "standouts", "adaptive_flexibility_change"):
        require(isinstance(record.get(key), dict), f"{key} must be an object")
    areas = record.get("areas")
    require(isinstance(areas, list) and len(areas) == 5, "areas must contain exactly five records")
    by_id = {area.get("id"): area for area in areas if isinstance(area, dict)}
    require(set(by_id) == set(AREA_ORDER), "areas must contain each required id exactly once")
    for area_id, area in by_id.items():
        display, research = EXPECTED_LABELS[area_id]
        require(area.get("display_label") == display, f"{area_id}.display_label must be {display!r}")
        require(area.get("research_label") == research, f"{area_id}.research_label must be {research!r}")
        require(area.get("level") in RATINGS, f"{area_id}.level must be 1–5 or null")
        require(area.get("evidence_strength") in {"low", "medium", "high"}, f"invalid evidence strength for {area_id}")
        for key in ("observed_pattern", "rating_rationale", "recommended_action"):
            require(isinstance(area.get(key), str) and area[key].strip(), f"{area_id}.{key} is required")
        require(isinstance(area.get("evidence", []), list) and len(area["evidence"]) <= 2, f"{area_id}.evidence allows at most two examples")
    inventory = record["evidence_inventory"]
    require(inventory.get("reviewed_count", 0) <= inventory.get("inventoried_count", -1), "reviewed_count cannot exceed inventoried_count")
    change = record["adaptive_flexibility_change"]
    require(change.get("status") in {"supported", "not-enough-evidence"}, "invalid adaptive_flexibility_change.status")
    if change["status"] == "supported":
        for key in ("friction", "changed_approach", "verified_result", "later_reuse"):
            require(isinstance(change.get(key), str) and change[key].strip(), f"supported change requires {key}")
    return by_id


def list_text(items: list[str], empty: str) -> str:
    return "; ".join(esc(item) for item in items) if items else esc(empty)


def observations_html(items: list[str], empty: str) -> str:
    if not items:
        return f"<p>{esc(empty)}</p>"
    if len(items) == 1:
        return f"<p>{esc(items[0])}</p>"
    return '<ul class="evidence-list">' + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def safe_link(url: object) -> str | None:
    if not isinstance(url, str) or not url:
        return None
    parsed = urlparse(url)
    return url if parsed.scheme in {"https", "http", "file"} or (not parsed.scheme and not url.startswith("//")) else None


def evidence_html(items: list[dict]) -> str:
    if not items:
        return '<p class="muted">No participant-facing example was available.</p>'
    rows = []
    for item in items[:2]:
        context = f"{item.get('date', '')} · {item.get('task_label', '')}".strip(" ·")
        label = esc(item.get("source_label") or context)
        url = safe_link(item.get("source_url"))
        source = f'<a href="{esc(url)}">{label}</a>' if url else label
        rows.append(f"<li><strong>{source}</strong> — {esc(item.get('summary', ''))}</li>")
    return '<ul class="evidence-list">' + "".join(rows) + "</ul>"


def snapshot_row(area: dict, change: dict) -> str:
    level = area["level"] or 0
    segment_class = " insufficient" if area["level"] is None else ""
    bars = "".join(f'<span class="segment{" on" if index <= level else ""}{segment_class}" aria-hidden="true"></span>' for index in range(1, 6))
    note = f'{area["evidence_strength"].title()} evidence'
    if area["id"] == "adaptive-flexibility" and change["status"] != "supported":
        note += " · Change over time not established"
    return f'''<div class="snapshot-row"><div class="area-name"><strong>{esc(area["display_label"])}</strong><small>{esc(area["research_label"])}</small></div><div class="segments" role="img" aria-label="{esc(area["display_label"])}: {esc(RATINGS[area["level"]])}; {esc(note)}">{bars}</div><div class="pattern"><strong class="rating">{esc(RATINGS[area["level"]])}</strong><small>{esc(note)}</small></div></div>'''


def detail_card(area: dict, open_by_default: bool) -> str:
    open_attribute = " open" if open_by_default else ""
    return f'''<details class="detail"{open_attribute}><summary><h3 class="detail__label">{esc(area["research_label"])}<small>{esc(area["display_label"])}</small></h3><span class="detail__meta"><strong class="rating">{esc(RATINGS[area["level"]])}</strong><small>{esc(area["evidence_strength"].title())} evidence</small></span></summary><div class="detail-grid"><div class="field"><span class="field__label">What we observed</span><p>{esc(area["observed_pattern"])}</p></div><div class="field"><span class="field__label">Where it was inconsistent</span>{observations_html(area.get("inconsistent_patterns", []), "No contradictory behavior was visible in the records reviewed.")}</div><div class="field wide"><span class="field__label">What we could not observe</span>{observations_html(area.get("evidence_gaps", []), "No material evidence gap was identified in the authorized records.")}</div><div class="field wide"><span class="field__label">Example</span>{evidence_html(area.get("evidence", []))}</div><div class="field wide try"><span class="field__label">Next action</span><p>{esc(area["recommended_action"])}</p></div></div></details>'''


def change_html(change: dict) -> str:
    if change["status"] != "supported":
        return f'<div class="change"><h3>Learn and adapt</h3><p>{esc("Not enough evidence to evaluate change over time.")}</p><p class="muted">{esc(change.get("summary", ""))}</p></div>'
    fields = [("Friction", change["friction"]), ("Changed approach", change["changed_approach"]), ("Checked result", change["verified_result"]), ("Later reuse", change["later_reuse"])]
    cells = "".join(f'<div class="field"><span class="field__label">{esc(label)}</span><p>{esc(value)}</p></div>' for label, value in fields)
    return f'<div class="change"><h3>Learn and adapt</h3><p>{esc(change["summary"])}</p><div class="change-grid">{cells}</div>{evidence_html(change.get("evidence", []))}</div>'


def render(record: dict, template: str) -> str:
    areas = validate(record)
    meta = record["meta"]
    standouts = record["standouts"]
    inventory = record["evidence_inventory"]
    reliability = record["reliability"]
    standout_cards = [
        ("Strongest observed habit", standouts["strongest_observed_habit"]),
        ("Current focus", standouts["current_focus"]),
        ("Try next", standouts["try_next"]),
    ]
    standouts_html = "".join(f'<div class="standout"><span class="standout__label">{esc(label)}</span><p>{esc(value)}</p></div>' for label, value in standout_cards)
    limits = list(reliability.get("limitations", [])) + list(inventory.get("access_limits", [])) + list(inventory.get("attribution_limits", []))
    attribution = list_text(inventory.get("attribution_limits", []), "Human attribution was available for the behavior used in ratings.")
    about = f'''<div class="about"><div class="about-grid"><div><strong>Evidence strength</strong><span>{esc(reliability["evidence_strength"].title())}</span></div><div><strong>Review period</strong><span>{esc(meta["review_period"])}</span></div><div><strong>Sources</strong><span>{list_text(inventory["source_types"], "No source types recorded")}</span></div><div><strong>Coverage</strong><span>{esc(inventory["reviewed_count"])} of {esc(inventory["inventoried_count"])} {esc(inventory["unit"])}s reviewed</span></div><div><strong>Selection</strong><span>{esc(inventory["sampling_method"])}</span></div><div><strong>Attribution</strong><span>{attribution}</span></div></div><div><strong>What we could not observe</strong>{observations_html(limits, "No material limit was identified in the authorized evidence.")}</div></div>'''
    replacements = {
        "{{DOCUMENT_TITLE}}": esc(meta["title"]),
        "{{TITLE}}": esc(meta["title"]),
        "{{GENERATED_ON}}": esc(meta["generated_on"]),
        "{{REVIEW_PERIOD}}": esc(meta["review_period"]),
        "{{COVERAGE_LINE}}": esc(meta["coverage_line"]),
        "{{STANDOUTS}}": standouts_html,
        "{{SNAPSHOT}}": "".join(snapshot_row(areas[key], record["adaptive_flexibility_change"]) for key in AREA_ORDER),
        "{{AREA_DETAILS}}": "".join(detail_card(areas[key], index == 0) for index, key in enumerate(DETAIL_IDS)),
        "{{ADAPTIVE_CHANGE}}": change_html(record["adaptive_flexibility_change"]),
        "{{ABOUT}}": about,
    }
    output = template
    for token, value in replacements.items():
        output = output.replace(token, value)
    require("{{" not in output, "unresolved template token")
    return output


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: render_report.py assessment.json report.html", file=sys.stderr)
        return 2
    source, destination = map(Path, sys.argv[1:])
    try:
        record = json.loads(source.read_text(encoding="utf-8"))
        template = (Path(__file__).parent.parent / "assets" / "report-template.html").read_text(encoding="utf-8")
        destination.write_text(render(record, template), encoding="utf-8")
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"render failed: {exc}", file=sys.stderr)
        return 1
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
