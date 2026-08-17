#!/usr/bin/env python3
"""Render a self-contained AI fluency review from assessment JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_IDS = {
    "description",
    "delegation",
    "discernment",
    "diligence",
    "adaptive-flexibility",
}
CONFIDENCE_LEVELS = {"low", "medium", "high"}
EVENT_ACTIONS = {
    "artifact_open",
    "source_open",
    "action_click",
    "edit",
    "comment",
    "approve",
    "reject",
    "rerun",
    "download",
    "share",
    "other",
}
EVENT_ACTORS = {"human", "agent", "mixed", "unknown"}
ACTOR_BASES = {
    "explicit_authorship",
    "tracked_change",
    "event_origin",
    "session_attribution",
    "inferred",
    "unknown",
}


def fail(message: str) -> None:
    raise ValueError(message)


def require_object(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{path} must be an object")
    return value


def require_text(value: Any, path: str, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        fail(f"{path} must be a string")
    if not allow_empty and not value.strip():
        fail(f"{path} must not be empty")
    return value.strip()


def require_score(value: Any, path: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value not in range(1, 6):
        fail(f"{path} must be null or a whole number from 1 to 5")
    return value


def require_choice(value: Any, path: str, choices: set[str], default: str | None = None) -> str:
    if value is None and default is not None:
        return default
    checked = require_text(value, path).lower()
    if checked not in choices:
        fail(f"{path} must be one of: {', '.join(sorted(choices))}")
    return checked


def validate_text_list(value: Any, path: str) -> list[str]:
    if not isinstance(value, list):
        fail(f"{path} must be an array")
    return [require_text(item, f"{path}[{index}]") for index, item in enumerate(value)]


def validate_events(value: Any) -> list[dict[str, str]]:
    if value is None:
        return []
    if not isinstance(value, list):
        fail("interaction_events must be an array")
    result: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        path = f"interaction_events[{index}]"
        obj = require_object(item, path)
        event_id = require_text(obj.get("id", ""), f"{path}.id")
        if event_id in seen:
            fail(f"duplicate interaction event id: {event_id}")
        seen.add(event_id)
        event = {
            "id": event_id,
            "timestamp": require_text(obj.get("timestamp", ""), f"{path}.timestamp"),
            "action": require_choice(obj.get("action"), f"{path}.action", EVENT_ACTIONS),
            "artifact_id": require_text(obj.get("artifact_id", ""), f"{path}.artifact_id"),
            "actor": require_choice(obj.get("actor"), f"{path}.actor", EVENT_ACTORS),
            "actor_basis": require_choice(
                obj.get("actor_basis"), f"{path}.actor_basis", ACTOR_BASES
            ),
            "provenance_confidence": require_choice(
                obj.get("provenance_confidence"),
                f"{path}.provenance_confidence",
                CONFIDENCE_LEVELS,
            ),
            "summary": require_text(obj.get("summary", ""), f"{path}.summary"),
            "source": require_text(obj.get("source", ""), f"{path}.source", allow_empty=True),
            "diff_ref": require_text(
                obj.get("diff_ref", ""), f"{path}.diff_ref", allow_empty=True
            ),
        }
        if event["action"] == "edit" and event["actor"] == "human":
            if event["actor_basis"] in {"inferred", "unknown"}:
                fail(f"{path}: a human edit needs a direct attribution basis")
        result.append(event)
    return result


def validate_evidence(value: Any, path: str) -> list[dict[str, str]]:
    if not isinstance(value, list):
        fail(f"{path} must be an array")
    if len(value) > 2:
        fail(f"{path} must contain no more than two examples")
    result: list[dict[str, str]] = []
    for index, item in enumerate(value):
        obj = require_object(item, f"{path}[{index}]")
        result.append(
            {
                "date": require_text(obj.get("date", ""), f"{path}[{index}].date"),
                "summary": require_text(obj.get("summary", ""), f"{path}[{index}].summary"),
                "source": require_text(
                    obj.get("source", ""), f"{path}[{index}].source", allow_empty=True
                ),
            }
        )
    return result


def validate_period(value: Any, path: str) -> dict[str, Any]:
    obj = require_object(value, path)
    evidence = obj.get("evidence")
    checked_evidence = None
    if evidence is not None:
        items = validate_evidence([evidence], f"{path}.evidence")
        checked_evidence = items[0]
    return {
        "period": require_text(obj.get("period", ""), f"{path}.period"),
        "score": require_score(obj.get("score"), f"{path}.score"),
        "confidence": require_choice(
            obj.get("confidence"), f"{path}.confidence", CONFIDENCE_LEVELS, default="low"
        ),
        "summary": require_text(obj.get("summary", ""), f"{path}.summary", allow_empty=True),
        "evidence": checked_evidence,
    }


def validate(data: Any) -> dict[str, Any]:
    root = require_object(data, "root")
    meta = require_object(root.get("meta"), "meta")
    reliability = require_object(root.get("reliability", {}), "reliability")
    events = validate_events(root.get("interaction_events", []))
    areas = root.get("areas")
    if not isinstance(areas, list):
        fail("areas must be an array")
    if len(areas) != 5:
        fail("areas must contain exactly five objects")

    checked_areas: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(areas):
        path = f"areas[{index}]"
        obj = require_object(item, path)
        area_id = require_text(obj.get("id", ""), f"{path}.id")
        if area_id not in REQUIRED_IDS:
            fail(f"{path}.id is not a supported area id")
        if area_id in seen:
            fail(f"duplicate area id: {area_id}")
        seen.add(area_id)
        checked_areas.append(
            {
                "id": area_id,
                "label": require_text(obj.get("label", ""), f"{path}.label"),
                "definition": require_text(obj.get("definition", ""), f"{path}.definition"),
                "score": require_score(obj.get("score"), f"{path}.score"),
                "confidence": require_choice(
                    obj.get("confidence"),
                    f"{path}.confidence",
                    CONFIDENCE_LEVELS,
                    default="low",
                ),
                "strength": require_text(
                    obj.get("strength", ""), f"{path}.strength", allow_empty=True
                ),
                "practice": require_text(
                    obj.get("practice", ""), f"{path}.practice", allow_empty=True
                ),
                "next_step": require_text(
                    obj.get("next_step", ""), f"{path}.next_step", allow_empty=True
                ),
                "evidence": validate_evidence(obj.get("evidence", []), f"{path}.evidence"),
            }
        )
    if seen != REQUIRED_IDS:
        fail(f"areas must contain these ids: {', '.join(sorted(REQUIRED_IDS))}")

    adaptive = require_object(root.get("adaptive_flexibility"), "adaptive_flexibility")
    return {
        "meta": {
            "title": require_text(meta.get("title", "AI Fluency Review"), "meta.title"),
            "summary": require_text(meta.get("summary", ""), "meta.summary", allow_empty=True),
            "generated_on": require_text(
                meta.get("generated_on", ""), "meta.generated_on", allow_empty=True
            ),
            "coverage_note": require_text(
                meta.get("coverage_note", ""), "meta.coverage_note", allow_empty=True
            ),
        },
        "reliability": {
            "confidence": require_choice(
                reliability.get("confidence"),
                "reliability.confidence",
                CONFIDENCE_LEVELS,
                default="low",
            ),
            "coverage_summary": require_text(
                reliability.get("coverage_summary", ""),
                "reliability.coverage_summary",
                allow_empty=True,
            ),
            "limitations": validate_text_list(
                reliability.get("limitations", []), "reliability.limitations"
            ),
        },
        "interaction_events": events,
        "areas": checked_areas,
        "adaptive_flexibility": {
            "baseline": validate_period(adaptive.get("baseline"), "adaptive_flexibility.baseline"),
            "recent": validate_period(adaptive.get("recent"), "adaptive_flexibility.recent"),
        },
    }


def presentation_payload(report: dict[str, Any]) -> dict[str, Any]:
    """Return only fields safe and useful for the standalone report."""
    events = report["interaction_events"]
    actor_counts = {actor: 0 for actor in EVENT_ACTORS}
    attributed_edits = 0
    unattributed_edits = 0
    for event in events:
        actor_counts[event["actor"]] += 1
        if event["action"] == "edit":
            direct = event["actor_basis"] not in {"inferred", "unknown"}
            if event["actor"] != "unknown" and direct:
                attributed_edits += 1
            else:
                unattributed_edits += 1

    return {
        "meta": report["meta"],
        "reliability": {
            **report["reliability"],
            "event_count": len(events),
            "human_events": actor_counts["human"],
            "agent_events": actor_counts["agent"],
            "mixed_events": actor_counts["mixed"],
            "unknown_events": actor_counts["unknown"],
            "attributed_edits": attributed_edits,
            "unattributed_edits": unattributed_edits,
        },
        "areas": [
            {
                key: area[key]
                for key in (
                    "id",
                    "label",
                    "definition",
                    "score",
                    "confidence",
                    "strength",
                    "practice",
                    "next_step",
                )
            }
            for area in report["areas"]
        ],
        "adaptive_flexibility": {
            name: {
                key: period[key]
                for key in ("period", "score", "confidence", "summary")
            }
            for name, period in report["adaptive_flexibility"].items()
        },
    }


HTML = r'''<!doctype html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Fluency Review</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f4f0e7;
      --surface: #fffdf8;
      --surface-2: #f0ece3;
      --text: #26312b;
      --muted: #687169;
      --line: #d8d2c5;
      --accent: #718269;
      --good: #2f8a69;
      --good-soft: #dcefe6;
      --watch: #ad6843;
      --watch-soft: #fae6d8;
      --shadow: 0 18px 38px rgba(64, 57, 43, .08);
    }
    :root[data-theme="dark"] {
      color-scheme: dark;
      --bg: #111713;
      --surface: #1c241e;
      --surface-2: #242d26;
      --text: #f4f0e7;
      --muted: #bdc3ba;
      --line: #3d493f;
      --accent: #aebd9e;
      --good: #68d3aa;
      --good-soft: #174d3c;
      --watch: #f0a474;
      --watch-soft: #5b3422;
      --shadow: 0 18px 38px rgba(0, 0, 0, .2);
    }
    * { box-sizing: border-box; }
    html { font-family: ui-rounded, "Avenir Next", system-ui, sans-serif; background: var(--bg); color: var(--text); }
    body { margin: 0; background: var(--bg); }
    button, table { font: inherit; }
    .page { width: min(100% - 32px, 1160px); margin: 0 auto; padding: 38px 0 70px; }
    .top { display: flex; justify-content: flex-end; margin-bottom: 24px; }
    .theme { display: inline-flex; gap: 3px; padding: 4px; border: 1px solid var(--line); border-radius: 999px; background: var(--surface-2); }
    .theme button { border: 0; border-radius: 999px; padding: 8px 18px; color: var(--muted); background: transparent; cursor: pointer; }
    .theme button[aria-pressed="true"] { color: var(--text); background: var(--surface); box-shadow: 0 2px 7px rgba(0,0,0,.08); }
    header { margin-bottom: 28px; }
    h1 { max-width: 850px; margin: 0; font-size: clamp(2.5rem, 6vw, 5rem); line-height: .98; letter-spacing: -.055em; }
    .summary { max-width: 820px; margin: 18px 0 0; color: var(--muted); font-size: 1.1rem; }
    .date { margin-top: 12px; color: var(--muted); font-size: .84rem; }
    .panel { margin-top: 22px; padding: clamp(22px, 4vw, 42px); border: 1px solid var(--line); border-radius: 24px; background: var(--surface); box-shadow: var(--shadow); }
    h2 { margin: 0 0 24px; font-size: clamp(1.55rem, 3vw, 2.1rem); letter-spacing: -.03em; }
    h3 { margin: 0; font-size: 1.2rem; }
    .chart-wrap { min-height: 350px; }
    svg { display: block; width: 100%; overflow: visible; }
    .callout { display: grid; grid-template-columns: auto 1fr; gap: 14px; align-items: center; margin: 6px 0 18px; padding: 14px 16px; border-left: 4px solid var(--good); border-radius: 0 12px 12px 0; background: var(--good-soft); }
    .callout strong { color: var(--good); font-size: 1.12rem; white-space: nowrap; }
    .callout span { color: var(--muted); }
    .reliability-head { display: flex; justify-content: space-between; gap: 14px; align-items: center; margin-bottom: 18px; }
    .reliability-head h2 { margin: 0; }
    .confidence { display: inline-flex; align-items: center; padding: 5px 10px; border-radius: 999px; color: var(--good); background: var(--good-soft); font-size: .76rem; font-weight: 800; text-transform: capitalize; }
    .confidence.low { color: var(--watch); background: var(--watch-soft); }
    .reliability-copy { margin: 0 0 18px; color: var(--muted); }
    .reliability-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; }
    .metric { padding: 14px; border: 1px solid var(--line); border-radius: 14px; background: var(--surface-2); }
    .metric strong { display: block; font-size: 1.45rem; }
    .metric span { color: var(--muted); font-size: .78rem; }
    .limitations { margin: 14px 0 0; padding-left: 20px; color: var(--muted); font-size: .84rem; }
    table { width: 100%; border-collapse: collapse; font-size: .9rem; }
    th, td { padding: 11px 12px; border-top: 1px solid var(--line); text-align: left; vertical-align: top; }
    thead th { color: var(--muted); font-size: .75rem; letter-spacing: .04em; text-transform: uppercase; }
    td:nth-child(2) { color: var(--accent); font-weight: 750; }
    .advice-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
    .advice { padding: 20px; border: 1px solid var(--line); border-radius: 16px; background: var(--surface-2); }
    .advice:last-child { grid-column: 1 / -1; }
    .advice-head { display: flex; justify-content: space-between; gap: 12px; align-items: center; margin-bottom: 16px; }
    .chips { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; justify-content: flex-end; }
    .tag { padding: 4px 9px; border-radius: 999px; color: var(--good); background: var(--good-soft); font-size: .74rem; font-weight: 800; }
    .tag.watch { color: var(--watch); background: var(--watch-soft); }
    .advice dl { display: grid; grid-template-columns: 86px 1fr; gap: 9px 12px; margin: 0; }
    dt { color: var(--muted); font-weight: 750; }
    dd { margin: 0; }
    .definitions { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 10px; }
    .definition { padding: 16px; border: 1px solid var(--line); border-radius: 14px; background: var(--surface-2); }
    .definition h3 { font-size: 1rem; }
    .definition p { margin: 6px 0 0; color: var(--muted); font-size: .84rem; }
    .coverage { margin: 24px 0 0; color: var(--muted); font-size: .84rem; }
    .missing { color: var(--muted); font-style: italic; }
    @media (max-width: 640px) {
      .page { width: min(100% - 20px, 1160px); padding-top: 24px; }
      .top { justify-content: stretch; }
      .theme { width: 100%; }
      .theme button { flex: 1; }
      .panel { padding: 20px; border-radius: 17px; }
      .advice-grid, .definitions, .reliability-grid { grid-template-columns: 1fr; }
      .advice:last-child { grid-column: auto; }
      .advice dl { grid-template-columns: 76px 1fr; }
      .callout { grid-template-columns: 1fr; gap: 3px; }
      .change-table thead { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }
      .change-table, .change-table tbody, .change-table tr, .change-table th, .change-table td { display: block; width: 100%; }
      .change-table tbody { display: grid; gap: 12px; }
      .change-table tr { padding: 14px; border: 1px solid var(--line); border-radius: 12px; background: var(--surface-2); }
      .change-table th, .change-table td { padding: 4px 0; border: 0; }
      .change-table td[data-label]::before { content: attr(data-label); display: block; margin-bottom: 2px; color: var(--muted); font-size: .7rem; font-weight: 750; letter-spacing: .04em; text-transform: uppercase; }
    }
    @media print { :root { color-scheme: light; } body { background: #fff; } .page { width: 100%; padding: 0; } .top { display: none; } .panel { box-shadow: none; break-inside: avoid; } }
  </style>
</head>
<body>
  <main class="page">
    <div class="top">
      <div class="theme" aria-label="Color theme">
        <button type="button" data-theme="light" aria-pressed="true">Light</button>
        <button type="button" data-theme="dark" aria-pressed="false">Dark</button>
      </div>
    </div>
    <header>
      <h1 id="report-title"></h1>
      <p class="summary" id="report-summary" hidden></p>
      <p class="date" id="report-date" hidden></p>
    </header>

    <section class="panel" aria-labelledby="definitions-heading">
      <h2 id="definitions-heading">Five Areas</h2>
      <div class="definitions" id="definitions"></div>
    </section>

    <section class="panel" aria-labelledby="overview-heading">
      <h2 id="overview-heading">Your five AI fluency areas</h2>
      <div class="chart-wrap"><svg id="overview-chart" role="img"></svg></div>
    </section>

    <section class="panel" aria-labelledby="reliability-heading">
      <div class="reliability-head"><h2 id="reliability-heading">Reliability</h2><span class="confidence" id="overall-confidence"></span></div>
      <p class="reliability-copy" id="reliability-copy"></p>
      <div class="reliability-grid" id="reliability-grid"></div>
      <ul class="limitations" id="limitations" hidden></ul>
    </section>

    <section class="panel" aria-labelledby="adaptive-heading">
      <h2 id="adaptive-heading">Adaptive flexibility</h2>
      <div class="chart-wrap"><svg id="adaptive-chart" role="img"></svg></div>
      <div class="callout" id="change-callout"></div>
      <table class="change-table">
        <thead><tr><th>Period</th><th>Evaluation</th><th>What changed</th><th>Confidence</th></tr></thead>
        <tbody id="change-rows"></tbody>
      </table>
    </section>

    <section class="panel" aria-labelledby="actions-heading">
      <h2 id="actions-heading">What to keep and what to practice</h2>
      <div class="advice-grid" id="advice-grid"></div>
    </section>

    <p class="coverage" id="coverage" hidden></p>
  </main>

  <script>
    const report = __REPORT_DATA__;
    const labels = {1:"Needs work",2:"Developing",3:"Moderate",4:"Strong",5:"Very strong"};
    const esc = value => String(value ?? "").replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"})[char]);
    const rating = score => score == null ? "Not enough evidence" : labels[score];

    document.title = report.meta.title;
    document.getElementById("report-title").textContent = report.meta.title;
    if (report.meta.summary) {
      const node = document.getElementById("report-summary");
      node.textContent = report.meta.summary;
      node.hidden = false;
    }
    if (report.meta.generated_on) {
      const node = document.getElementById("report-date");
      node.textContent = `Prepared ${report.meta.generated_on}`;
      node.hidden = false;
    }
    if (report.meta.coverage_note) {
      const node = document.getElementById("coverage");
      node.textContent = report.meta.coverage_note;
      node.hidden = false;
    }

    const overviewSvg = document.getElementById("overview-chart");
    const adaptiveSvg = document.getElementById("adaptive-chart");

    function colors() {
      const style = getComputedStyle(document.documentElement);
      return Object.fromEntries(["text","muted","line","accent","good","watch","surface"].map(name => [name, style.getPropertyValue(`--${name}`).trim()]));
    }

    function renderOverview() {
      const width = Math.max(300, overviewSvg.parentElement.clientWidth);
      const mobile = width < 620;
      const height = mobile ? 365 : 350;
      const margin = mobile ? {top:34,right:10,bottom:108,left:78} : {top:38,right:28,bottom:82,left:116};
      const innerW = width - margin.left - margin.right;
      const innerH = height - margin.top - margin.bottom;
      const bandW = innerW / report.areas.length;
      const barW = Math.min(mobile ? 40 : 88, bandW * .58);
      const x = index => margin.left + bandW * index + bandW / 2;
      const y = score => margin.top + innerH - (score / 5 * innerH);
      const c = colors();
      overviewSvg.setAttribute("viewBox", `0 0 ${width} ${height}`);
      overviewSvg.setAttribute("height", height);
      overviewSvg.setAttribute("aria-label", report.areas.map(area => `${area.label}: ${rating(area.score)}`).join(". "));
      overviewSvg.innerHTML = `
        <title>Current evaluation of five AI fluency areas</title>
        ${[1,2,3,4,5].map(score => `<line x1="${margin.left}" y1="${y(score)}" x2="${width-margin.right}" y2="${y(score)}" stroke="${c.line}"/><text x="${margin.left-12}" y="${y(score)+4}" text-anchor="end" fill="${c.muted}" font-size="${mobile?10:12}">${labels[score]}</text>`).join("")}
        ${report.areas.map((area,index) => {
          const score = area.score;
          const barY = score == null ? y(0) : y(score);
          const fill = score === 3 ? c.watch : score === 5 ? c.accent : c.good;
          const bar = score == null
            ? `<line x1="${x(index)-barW/2}" y1="${y(0)}" x2="${x(index)+barW/2}" y2="${y(0)}" stroke="${c.muted}" stroke-width="3" stroke-dasharray="4 4"/>`
            : `<rect x="${x(index)-barW/2}" y="${barY}" width="${barW}" height="${y(0)-barY}" rx="${mobile?6:9}" fill="${fill}" opacity=".82"/>`;
          const valueY = score == null ? y(0)-10 : barY-10;
          const axisLabel = mobile
            ? `<text x="${x(index)}" y="${height-24}" transform="rotate(-42 ${x(index)} ${height-24})" text-anchor="end" fill="${c.text}" font-size="10" font-weight="700">${esc(area.label)}</text>`
            : `<text x="${x(index)}" y="${height-42}" text-anchor="middle" fill="${c.text}" font-size="12" font-weight="700">${esc(area.label)}</text>`;
          return `<g class="overview-bar"><title>${esc(area.label)}: ${rating(score)}</title>${bar}<text x="${x(index)}" y="${valueY}" text-anchor="middle" fill="${c.text}" font-size="${mobile?9:12}" font-weight="750">${score == null && mobile ? "No evidence" : rating(score)}</text>${axisLabel}</g>`;
        }).join("")}`;
    }

    function renderAdaptive() {
      const width = Math.max(300, adaptiveSvg.parentElement.clientWidth);
      const mobile = width < 620;
      const height = mobile ? 270 : 280;
      const margin = mobile ? {top:28,right:18,bottom:46,left:108} : {top:30,right:42,bottom:46,left:145};
      const innerW = width-margin.left-margin.right;
      const innerH = height-margin.top-margin.bottom;
      const x = index => margin.left + innerW*index;
      const y = score => margin.top + innerH - ((score-1)/4*innerH);
      const points = [report.adaptive_flexibility.baseline, report.adaptive_flexibility.recent];
      const c = colors();
      adaptiveSvg.setAttribute("viewBox", `0 0 ${width} ${height}`);
      adaptiveSvg.setAttribute("height", height);
      adaptiveSvg.setAttribute("aria-label", points.map(point => `${point.period}: ${rating(point.score)}`).join(". "));
      const valid = points.map((point,index) => ({...point,index})).filter(point => point.score != null);
      const connector = valid.length === 2 ? `<line x1="${x(0)}" y1="${y(valid[0].score)}" x2="${x(1)}" y2="${y(valid[1].score)}" stroke="${c.accent}" stroke-width="3" stroke-linecap="round"/>` : "";
      adaptiveSvg.innerHTML = `
        <title>Adaptive flexibility over time</title>
        ${[1,2,3,4,5].map(score => `<line x1="${margin.left}" y1="${y(score)}" x2="${width-margin.right}" y2="${y(score)}" stroke="${c.line}"/><text x="${margin.left-12}" y="${y(score)+4}" text-anchor="end" fill="${c.muted}" font-size="12">${labels[score]}</text>`).join("")}
        ${connector}
        ${points.map((point,index) => point.score == null
          ? `<text x="${x(index)}" y="${margin.top+innerH/2}" text-anchor="${index===0?"start":"end"}" fill="${c.muted}" font-size="12">Not enough evidence</text>`
          : `<circle cx="${x(index)}" cy="${y(point.score)}" r="8" fill="${index===0?c.surface:c.accent}" stroke="${index===0?c.muted:c.accent}" stroke-width="3"/><text x="${x(index)}" y="${y(point.score)-16}" text-anchor="${index===0?"start":"end"}" fill="${c.text}" font-size="12" font-weight="750">${rating(point.score)}</text>`).join("")}
        ${points.map((point,index) => `<text x="${x(index)}" y="${height-18}" text-anchor="${index===0?"start":"end"}" fill="${c.text}" font-size="12" font-weight="700">${esc(point.period)}</text>`).join("")}`;

      const baseline = points[0].score;
      const recent = points[1].score;
      const callout = document.getElementById("change-callout");
      if (baseline == null || recent == null) {
        callout.innerHTML = `<strong>Trend unavailable</strong><span>The two periods do not contain enough comparable evidence.</span>`;
      } else {
        const delta = recent-baseline;
        const deltaLabel = delta > 0 ? `+${delta} level${delta===1?"":"s"}` : delta < 0 ? `${delta} level${delta===-1?"":"s"}` : "No level change";
        const interpretation = delta > 0 ? "Recent behavior shows a stronger learning loop." : delta < 0 ? "Recent behavior shows less consistent adaptation." : "The evaluation stayed at the same level across both periods.";
        callout.innerHTML = `<strong>${deltaLabel}</strong><span>${interpretation}</span>`;
      }
    }

    function renderDetails() {
      const periods = [report.adaptive_flexibility.baseline, report.adaptive_flexibility.recent];
      document.getElementById("change-rows").innerHTML = periods.map(period => `<tr><th>${esc(period.period)}</th><td data-label="Evaluation">${rating(period.score)}</td><td data-label="What changed">${period.summary ? esc(period.summary) : '<span class="missing">Not enough evidence to interpret this period.</span>'}</td><td data-label="Confidence"><span class="confidence ${period.confidence}">${esc(period.confidence)}</span></td></tr>`).join("");

      document.getElementById("advice-grid").innerHTML = report.areas.map(area => `<article class="advice"><div class="advice-head"><h3>${esc(area.label)}</h3><div class="chips"><span class="tag ${area.score===3?"watch":""}">${rating(area.score)}</span><span class="confidence ${area.confidence}">${esc(area.confidence)} confidence</span></div></div><dl><dt>Keep</dt><dd>${area.strength ? esc(area.strength) : '<span class="missing">Not enough evidence</span>'}</dd><dt>Practice</dt><dd>${area.practice ? esc(area.practice) : '<span class="missing">Not enough evidence</span>'}</dd><dt>Try next</dt><dd>${area.next_step ? esc(area.next_step) : '<span class="missing">Add a next action after reviewing evidence</span>'}</dd></dl></article>`).join("");

      document.getElementById("definitions").innerHTML = report.areas.map(area => `<article class="definition"><h3>${esc(area.label)}</h3><p>${esc(area.definition)}</p></article>`).join("");

      const reliability = report.reliability;
      const overall = document.getElementById("overall-confidence");
      overall.className = `confidence ${reliability.confidence}`;
      overall.textContent = `${reliability.confidence} confidence`;
      document.getElementById("reliability-copy").textContent = reliability.coverage_summary || (reliability.event_count ? "Interaction records were checked for human and agent authorship." : "No interaction event log was supplied; confidence depends on the other authorized records.");
      const mixedUnknown = reliability.mixed_events + reliability.unknown_events;
      document.getElementById("reliability-grid").innerHTML = [
        [reliability.human_events, "Human-attributed actions"],
        [reliability.agent_events, "Agent-attributed actions"],
        [mixedUnknown, "Mixed or unknown actions"],
        [`${reliability.attributed_edits}/${reliability.attributed_edits + reliability.unattributed_edits}`, "Edits with attribution"]
      ].map(([value,label]) => `<div class="metric"><strong>${esc(value)}</strong><span>${esc(label)}</span></div>`).join("");
      if (reliability.limitations.length) {
        const limits = document.getElementById("limitations");
        limits.innerHTML = reliability.limitations.map(item => `<li>${esc(item)}</li>`).join("");
        limits.hidden = false;
      }
    }

    function setTheme(theme, persist=true) {
      const next = theme === "dark" ? "dark" : "light";
      document.documentElement.dataset.theme = next;
      document.querySelectorAll("[data-theme]").forEach(button => button.setAttribute("aria-pressed", String(button.dataset.theme===next)));
      if (persist) localStorage.setItem("ai-fluency-review-theme", next);
      requestAnimationFrame(() => { renderOverview(); renderAdaptive(); });
    }

    document.querySelector(".theme").addEventListener("click", event => {
      const button = event.target.closest("[data-theme]");
      if (button) setTheme(button.dataset.theme);
    });

    renderDetails();
    setTheme(localStorage.getItem("ai-fluency-review-theme") || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"), false);
    new ResizeObserver(renderOverview).observe(overviewSvg.parentElement);
    new ResizeObserver(renderAdaptive).observe(adaptiveSvg.parentElement);
  </script>
</body>
</html>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Assessment JSON")
    parser.add_argument("--output", required=True, type=Path, help="Destination HTML")
    args = parser.parse_args()

    try:
        raw = json.loads(args.input.read_text(encoding="utf-8"))
        report = presentation_payload(validate(raw))
    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.error(str(error))

    payload = json.dumps(report, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    output = HTML.replace("__REPORT_DATA__", payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
