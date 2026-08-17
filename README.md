# AI Fluency Review Skill

A vendor-neutral agent skill for creating concise, evidence-linked AI fluency reviews from authorized interaction records.

It assesses five observable areas:

- Description
- Delegation
- Discernment
- Diligence
- Adaptive Flexibility

The skill tells the agent how to create a self-contained light/dark HTML report with a five-area evaluation, an Adaptive Flexibility time comparison, practical next steps, and a concise reliability summary.

## Install

Copy `skills/ai-fluency-review` into the skill directory used by your agent harness. For Codex:

```bash
cp -R skills/ai-fluency-review ~/.codex/skills/ai-fluency-review
```

## Use

Ask the agent to use the skill with the records you authorize:

```text
Use the AI Fluency Review Skill to review these authorized AI-use records and create the HTML report.
```

You may also invoke it with the skill syntax supported by your agent or harness.

The optional assessment-record format is in [input-schema.md](skills/ai-fluency-review/references/input-schema.md). Scoring guidance is in [rubric.md](skills/ai-fluency-review/references/rubric.md).

## Principles

- Assess behavior, not personality.
- Separate human, agent, mixed, and unknown actions.
- Treat clicks and opens as interaction, not proof of understanding.
- Keep detailed evidence out of the HTML report.
- Do not use the review for automated ranking or employment decisions.

## License

[MIT](LICENSE)
