# AI Fluency Review Skill

A vendor-neutral agent skill for creating concise, evidence-linked AI fluency reviews from authorized interaction records.

The review covers five areas:

- Description
- Delegation
- Discernment
- Diligence
- Adaptive Flexibility

It produces a self-contained light/dark HTML report with:

- concise definitions before the evaluation;
- a five-area bar chart using a five-level rubric;
- an Adaptive Flexibility comparison across time;
- practical strengths, practice points, and next actions;
- aggregate reliability and human/agent attribution counts.

Raw evidence, source links, click trails, and edit records remain in the assessment JSON and are not embedded in the HTML.

## Reliability principles

- Opens and clicks show interaction, not understanding or authorship.
- Agent-only actions never raise the person's score.
- Human edits require a direct attribution basis, such as tracked changes or explicit authorship.
- Unknown-actor evidence cannot support the two highest ratings.
- A Very strong result requires repeated, high-confidence human evidence across at least three contexts.
- Missing or uneven evidence remains visible as a limitation.

See [Methodology](docs/methodology.md) and [Provenance and privacy](docs/provenance-and-privacy.md).

## Install

Copy the skill directory into the skill location used by your agent harness. For Codex:

```bash
cp -R skills/ai-fluency-review ~/.codex/skills/ai-fluency-review
```

For another harness, load `skills/ai-fluency-review/SKILL.md` with its `references`, `assets`, and `scripts` directories. The renderer uses only the Python standard library.

## Use

Ask the agent to use `$ai-fluency-review` with the records you authorize. Examples:

```text
Use $ai-fluency-review to compare my recent 7 days with the prior 14 days.
```

```text
Use $ai-fluency-review on these task records. Separate human edits from agent edits and create the HTML report.
```

To render an existing assessment:

```bash
python skills/ai-fluency-review/scripts/render_report.py \
  --input examples/minimal-assessment.json \
  --output ai_fluency_review.html
```

The assessment format is documented in [input-schema.md](skills/ai-fluency-review/references/input-schema.md). The scoring anchors are in [rubric.md](skills/ai-fluency-review/references/rubric.md).

## Responsible use

This is a formative behavioral review, not a validated psychometric test. In candidate or employee settings, obtain appropriate consent, limit collection and retention, and keep a human reviewer responsible for interpretation. Do not use it for automated ranking, hiring, promotion, pay, or discipline decisions.

## Validation

```bash
mise run validate
```

The validation renders the public example and confirms that detailed evidence is absent from the HTML.

## License

[MIT](LICENSE)
