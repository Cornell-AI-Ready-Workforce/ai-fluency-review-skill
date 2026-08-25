#!/usr/bin/env python3
"""Focused contract checks for the optional report renderer."""

from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
SPEC = importlib.util.spec_from_file_location("render_report", Path(__file__).with_name("render_report.py"))
assert SPEC and SPEC.loader
RENDERER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDERER)


class RendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.record = json.loads((ROOT / "examples" / "sample-assessment.json").read_text())
        cls.template = (ROOT / "assets" / "report-template.html").read_text()

    def render(self, record: dict | None = None) -> str:
        return RENDERER.render(record or copy.deepcopy(self.record), self.template)

    def test_renders_exactly_four_area_details(self) -> None:
        output = self.render()
        details = output.split('<section aria-labelledby="details">', 1)[1].split("</section>", 1)[0]
        self.assertEqual(details.count('<details class="detail"'), 4)
        self.assertNotIn("Learn and adapt</small>", details)
        self.assertEqual(details.count('<details class="detail" open>'), 1)

    def test_null_level_stays_not_enough_evidence(self) -> None:
        record = copy.deepcopy(self.record)
        record["areas"][0]["level"] = None
        output = self.render(record)
        self.assertIn("Brief the task: Not enough evidence", output)

    def test_private_ids_do_not_enter_html(self) -> None:
        output = self.render()
        self.assertNotIn("episode-002", output)
        self.assertNotIn("private_source_id", output)

    def test_source_content_is_escaped(self) -> None:
        record = copy.deepcopy(self.record)
        record["standouts"]["current_focus"] = '<script id="injected">alert(1)</script>'
        output = self.render(record)
        self.assertNotIn('<script id="injected">', output)
        self.assertIn("&lt;script id=&quot;injected&quot;&gt;", output)

    def test_unsupported_change_uses_required_sentence(self) -> None:
        output = self.render()
        self.assertIn("Not enough evidence to evaluate change over time.", output)

    def test_about_repeats_review_period(self) -> None:
        output = self.render()
        about = output.split('<section aria-labelledby="about">', 1)[1]
        self.assertIn(self.record["meta"]["review_period"], about)
        self.assertIn("Attribution", about)

    def test_snapshot_shows_evidence_strength(self) -> None:
        output = self.render()
        snapshot = output.split('<section aria-labelledby="snapshot">', 1)[1].split("</section>", 1)[0]
        self.assertIn("High evidence", snapshot)
        self.assertIn("Change over time not established", snapshot)

    def test_multiple_observations_render_as_a_list(self) -> None:
        output = self.render()
        self.assertNotIn(".;", output)
        self.assertIn("One scheduling request did not say which constraint mattered most", output)

    def test_rejects_duplicate_area(self) -> None:
        record = copy.deepcopy(self.record)
        record["areas"][4]["id"] = "description"
        with self.assertRaisesRegex(ValueError, "each required id exactly once"):
            self.render(record)


if __name__ == "__main__":
    unittest.main()
