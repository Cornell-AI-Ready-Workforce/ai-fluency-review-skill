# AI Fluency Review Skill

A minimal, vendor-neutral skill for creating a warm, private AI Use Report from records a person explicitly authorizes.

The skill reviews Description, Delegation, Discernment, Diligence, and Adaptive Flexibility. It compares directly with a previous report when available; otherwise it compares adjacent rolling 15-day periods.

## Install and create your report

Copy and send this message to your agent:

> Please install the AI Fluency Review skill from https://github.com/Cornell-AI-Ready-Workforce/ai-fluency-review-skill/tree/main/skills/ai-fluency-review.
>
> Use this app’s built-in skill or plugin installer. Do not ask me to use Terminal. If you need permission to download or install the skill, ask me in the app. Confirm when the skill is persistently installed. If this app cannot install custom skills, say so clearly and give me the exact click-only steps available in this app.
>
> After installation, use the skill to create my private, personalized AI-fluency report. Before reading anything, ask me which AI-use records and time period I authorize.

<details>
<summary>Advanced: install from Terminal</summary>

```sh
npx skills add Cornell-AI-Ready-Workforce/ai-fluency-review-skill -g
```

The installer detects supported agent hosts and installs the skill globally. Start a new agent session after installation.

</details>

<details>
<summary>Manual installation</summary>

Copy `skills/ai-fluency-review` into your agent host’s skill directory.

</details>

## Use

```text
Use $ai-fluency-review with the AI-assisted work records I authorize. Keep the report private.
```

The skill creates one self-contained HTML report.

## License

[MIT](LICENSE)
