# AI Fluency Review Skill

A private coaching report on how you work with AI, built by your own assistant from your own past sessions. It reviews five habits from the AI Fluency Framework: Description, Delegation, Discernment, Diligence, and Adaptive Flexibility.

It is written for you. It is not for ranking people or making employment decisions.

## Create your review

Copy this message and send it to Claude, ChatGPT, or any other AI assistant:

> Please install the AI Fluency Review skill from https://github.com/Cornell-AI-Ready-Workforce/ai-fluency-review-skill. If you cannot install skills, open that link, read `skills/ai-fluency-review/SKILL.md` and its report template, and follow them. Then create my private AI Fluency Review.

If your assistant cannot open links, paste the contents of [SKILL.md](skills/ai-fluency-review/SKILL.md) and [report-template.html](skills/ai-fluency-review/assets/report-template.html) into the chat instead, followed by: "Follow the pasted skill to create my private AI Fluency Review."

## What happens next

1. The assistant asks two questions and suggests answers: which records to use, with its own past conversations and saved memory as the default, and which period, with the last 30 days as the default. Reply "defaults" or change either.
2. It reads only what you confirmed. It does not open another AI tool's history unless you name it. Your records travel the same way as anything else you say to that assistant, and nowhere else.
3. Thirty days of history takes ten to thirty minutes.
4. You get one HTML file, `ai_fluency_review.html`, saved where the assistant can write or returned in the chat. It shows your strongest habit, your current focus, one action to try next, one row per habit, and dated examples in your own words, with a note on what was read and what was not.

Run it again in a month and give it the earlier file to compare against.

<details>
<summary>Install from a terminal</summary>

```sh
npx skills add Cornell-AI-Ready-Workforce/ai-fluency-review-skill -g
```

Or copy `skills/ai-fluency-review` into your agent's skill directory. Start a new session, then send: "Use the ai-fluency-review skill to create my private AI Fluency Review."

</details>

## License

[MIT](LICENSE)
