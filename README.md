# ai-fluency-review-skill

A minimal, vendor-neutral skill for creating a warm, private AI Use Report from records a person explicitly authorizes.

The skill reviews Description, Delegation, Discernment, Diligence, and Adaptive Flexibility. It compares directly with a previous report when available; otherwise it compares adjacent rolling 15-day periods. Missing comparison evidence is reported as not enough evidence.

## Install

```sh
npx skills add Cornell-AI-Ready-Workforce/ai-fluency-review-skill -g
```

The installer detects supported agent hosts and installs the skill globally. Start a new agent session after installation.

<details>
<summary>Manual installation</summary>

Copy `skills/ai-fluency-review` into your agent host’s skill directory.

</details>

## Use

```text
Use $ai-fluency-review with the AI-assisted work records I authorize. Keep the report private.
```

The skill creates one self-contained HTML report. It does not rank people or support employment decisions.

## License

[MIT](LICENSE)
