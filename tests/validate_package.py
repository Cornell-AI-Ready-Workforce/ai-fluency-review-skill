#!/usr/bin/env python3
"""Validate the public package without third-party dependencies."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "ai-fluency-review" / "SKILL.md"
REPORT = ROOT / "ai_fluency_review.html"
EXAMPLE = ROOT / "examples" / "minimal-assessment.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


skill_text = SKILL.read_text(encoding="utf-8")
report_text = REPORT.read_text(encoding="utf-8")
example = json.loads(EXAMPLE.read_text(encoding="utf-8"))

require(skill_text.startswith("---\nname: ai-fluency-review\n"), "skill name is invalid")
require("display_name: \"AI Fluency Review Skill\"" in (ROOT / "skills" / "ai-fluency-review" / "agents" / "openai.yaml").read_text(encoding="utf-8"), "display name is invalid")
require("Five Areas" in report_text, "definitions heading is missing")
require("Reliability" in report_text, "reliability section is missing")
require("private://" not in report_text, "private references leaked into HTML")
for event in example["interaction_events"]:
    require(event["summary"] not in report_text, "event summary leaked into HTML")
require('"human_events":2' in report_text, "human event count is incorrect")
require('"agent_events":1' in report_text, "agent event count is incorrect")
require('"attributed_edits":2' in report_text, "edit attribution count is incorrect")

print("Package validation passed")
