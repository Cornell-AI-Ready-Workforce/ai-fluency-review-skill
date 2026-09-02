# AI Fluency Review Skill

A minimal, vendor-neutral skill for creating a warm, private AI Fluency Review from records a person explicitly authorizes.

The skill reviews Description, Delegation, Discernment, Diligence, and Adaptive Flexibility. It first asks two setup questions and offers defaults: your assistant’s own past sessions and memory, and the last 30 days. It compares directly with a previous review when available; otherwise it compares the two halves of the chosen period.

## Install and create your review

Copy and send this message to your agent:

> Please install the AI Fluency Review skill from https://github.com/Cornell-AI-Ready-Workforce/ai-fluency-review-skill
>
> After installation, use the skill to create my private, personalized AI Fluency Review.

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

<details>
<summary>No install (claude.ai, Claude Desktop, ChatGPT)</summary>

Paste the contents of [SKILL.md](skills/ai-fluency-review/SKILL.md) and [report-template.html](skills/ai-fluency-review/assets/report-template.html) into the chat, then send:

> Follow the pasted AI Fluency Review skill to create my private, personalized AI Fluency Review.

</details>

## Use

```text
Use the ai-fluency-review skill to create my private AI Fluency Review.
```

The skill creates one self-contained HTML report.

## License

[MIT](LICENSE)
