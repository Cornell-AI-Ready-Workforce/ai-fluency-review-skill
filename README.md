# AI Fluency Review Skill

A vendor-neutral agent skill for creating a private, evidence-linked coaching review from AI-use records a person explicitly authorizes.

The review covers five observable areas:

- Description — Brief the task
- Delegation — Divide the work
- Discernment — Check the result
- Diligence — Finish responsibly
- Adaptive Flexibility — Learn and adapt

It produces a self-contained light/dark HTML report with no composite score or ranking. Four-D details describe current behavior; Adaptive Flexibility is treated separately as change over time.

## Install

Copy the skill into the skill directory used by your agent host. For Codex:

```bash
cp -R skills/ai-fluency-review ~/.codex/skills/ai-fluency-review
```

## Use

The skill is explicit-only. Invoke it and name the records it may use:

```text
Use $ai-fluency-review with the AI-assisted work records in this folder from the last 14 days. Keep the report private.
```

The agent can write the HTML directly. For a reproducible render, create the optional assessment JSON and run:

```bash
python skills/ai-fluency-review/scripts/render_report.py assessment.json ai_fluency_review.html
```

The renderer uses only the Python standard library. See [input-schema.md](skills/ai-fluency-review/references/input-schema.md) for the record contract and [rubric.md](skills/ai-fluency-review/references/rubric.md) for evidence rules.

## Boundaries

- Assess observed behavior, not personality or employability.
- Separate human, agent, mixed, and unknown actions.
- Treat clicks and opens as interaction, not proof of judgment.
- Keep detailed evidence out of the HTML report.
- Do not use the review for ranking or employment decisions.

## License

[MIT](LICENSE)
