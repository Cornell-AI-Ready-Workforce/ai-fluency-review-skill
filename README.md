# AI Fluency Review Skill

A private coaching report on how you work with AI, built by your own assistant from your accessible past sessions, or from your current task when history cannot be read. It reviews the four habits of the AI Fluency Framework, Description, Delegation, Discernment, and Diligence, plus Adaptive Flexibility, this review’s own measure of change over time.

It is written for you. It is not for ranking people or making employment decisions.

## Create your review

In any chat, new or existing, send this message:

> Open https://github.com/Cornell-AI-Ready-Workforce/ai-fluency-review-skill, read `skills/ai-fluency-review/SKILL.md` and its report template, and create my private AI Fluency Review. You may use this conversation, your saved memory, and your own available past chats with me from the last 30 days.

If your assistant cannot open links, paste the contents of [SKILL.md](skills/ai-fluency-review/SKILL.md) and [report-template.html](skills/ai-fluency-review/assets/report-template.html) into the chat instead, followed by: "Follow the pasted skill to create my private AI Fluency Review."

## What happens next

1. The assistant checks whether its tools can retrieve the history you authorized. It asks about sources or dates only if you have not already specified them. Installation does not add history access.
2. It reads only what you confirmed. It does not open another AI tool's history unless you name it. Your records travel the same way as anything else you say to that assistant, and nowhere else.
3. If history is unavailable, it reviews the current task and states that limit. If this is an empty chat, it asks which task to review; you can run the skill in an existing task conversation without transferring transcripts. A review of one task does not establish change over a month.
4. You get one HTML file, `ai_fluency_review.html`, saved where the assistant can write or returned in the chat. It shows your strongest habit, where you have room to grow, one action to try next, one row per area, and examples in your own words, dated when the history has dates, with a note on what was read and what was not.

Run it again in a month. Afterwards, ask the assistant to compare the new review with the earlier one.

<details>
<summary>Install from a terminal</summary>

```sh
npx skills add Cornell-AI-Ready-Workforce/ai-fluency-review-skill -g
```

Or copy `skills/ai-fluency-review` into your agent's skill directory. Start a new session, then send: "Use the ai-fluency-review skill to create my private AI Fluency Review."

</details>

## License

[MIT](LICENSE)
