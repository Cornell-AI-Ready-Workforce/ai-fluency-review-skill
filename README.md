# AI Use Report Skill

A minimal, vendor-neutral skill for creating a warm, private AI Use Report from records a person explicitly authorizes.

The skill reviews Description, Delegation, Discernment, Diligence, and Adaptive Flexibility. It compares directly with a previous report when available; otherwise it compares adjacent rolling 15-day periods. Missing comparison evidence is reported as not enough evidence.

## Install

Copy `skills/ai-fluency-review` into your agent host’s skill directory. The package contains only `SKILL.md` and one static HTML design template; it has no renderer, schema, tests, or application code.

## Use

```text
Use $ai-fluency-review with the AI-assisted work records I authorize. Keep the report private.
```

The skill creates one self-contained HTML report. It does not rank people or support employment decisions.

## License

[MIT](LICENSE)
