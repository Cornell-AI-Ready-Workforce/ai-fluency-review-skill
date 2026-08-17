# Assessment record

Use this optional JSON record when a separate, auditable assessment file is useful. The HTML report can be created directly without this file.

## Required shape

```json
{
  "meta": {
    "title": "AI Fluency Review",
    "summary": "Optional one-sentence finding.",
    "generated_on": "YYYY-MM-DD",
    "coverage_note": "Short note about sources and limits."
  },
  "reliability": {
    "confidence": "low | medium | high",
    "coverage_summary": "What evidence was available and attributable.",
    "limitations": []
  },
  "interaction_events": [],
  "areas": [],
  "adaptive_flexibility": {
    "baseline": {},
    "recent": {}
  }
}
```

## `areas`

Provide exactly one object for each required id: `description`, `delegation`, `discernment`, `diligence`, and `adaptive-flexibility`.

| Field | Type | Rule |
|---|---|---|
| `id` | string | One required id. |
| `label` | string | Human-readable area name. |
| `definition` | string | One plain-language sentence. |
| `score` | integer or null | Whole number 1–5, or null when evidence is insufficient. |
| `confidence` | string | `low`, `medium`, or `high`; this is confidence in the evidence, not the skill level. |
| `strength` | string | One observed positive behavior. |
| `practice` | string | One specific improvement. |
| `next_step` | string | One practical next action. |
| `evidence` | array | Zero to two evidence objects. |

An evidence object contains:

```json
{
  "date": "YYYY-MM-DD or a short period label",
  "summary": "One concise observed behavior.",
  "source": "Optional URL, relative path, file URL, or stable record id"
}
```

`source` is optional. Use a URL, relative path, file URL, or stable record identifier.

## `interaction_events`

Keep the detailed audit trail here. Put only aggregate counts in the HTML; do not embed event summaries, source references, or diff references in the page.

```json
{
  "id": "event-001",
  "timestamp": "YYYY-MM-DDThh:mm:ssZ or supplied time label",
  "action": "artifact_open",
  "artifact_id": "stable artifact id",
  "actor": "human",
  "actor_basis": "event_origin",
  "provenance_confidence": "high",
  "summary": "Opened the generated report.",
  "source": "optional private source reference",
  "diff_ref": "optional tracked-change or diff reference"
}
```

Allowed actions are `artifact_open`, `source_open`, `action_click`, `edit`, `comment`, `approve`, `reject`, `rerun`, `download`, `share`, and `other`. Allowed actors are `human`, `agent`, `mixed`, and `unknown`. Allowed attribution bases are `explicit_authorship`, `tracked_change`, `event_origin`, `session_attribution`, `inferred`, and `unknown`.

For edits, use `diff_ref` when available. Set `actor` to `mixed` when both human and agent contributed and the contributions cannot be cleanly separated. Do not relabel an unknown event as human simply because it happened in the person's session.

## `reliability`

| Field | Type | Rule |
|---|---|---|
| `confidence` | string | `low`, `medium`, or `high`, using the rubric reliability anchors. |
| `coverage_summary` | string | Concise account of periods, contexts, and attribution coverage. |
| `limitations` | array of strings | Material gaps only; do not hide unequal windows or unknown authorship. |

Derive event counts from `interaction_events`; do not enter manual counts.

## `adaptive_flexibility`

Both `baseline` and `recent` contain:

| Field | Type | Rule |
|---|---|---|
| `period` | string | Display label such as `Prior 14 days`. |
| `score` | integer or null | Whole number 1–5 or null. |
| `confidence` | string | `low`, `medium`, or `high`. |
| `summary` | string | What behavior in this period showed. |
| `evidence` | object or null | One concise evidence object. |

If either score is null, the report shows the available point and states that change cannot be evaluated reliably.

## Scoring and privacy rules

- Opens and clicks alone do not support a positive score; they only show interaction.
- Agent-only events cannot raise the person's score. Unknown-actor events cannot support a score of 4 or 5.
- A human-attributed revision, rejection, approval, verification, or reusable rule may support a score when its meaning is clear from the surrounding evidence.
- Keep evidence and event records in the assessment JSON only. Restrict access because the JSON may contain private activity records.
- For candidates or employees, obtain appropriate consent and define access and retention. Never use this report for automated ranking or a hiring decision.

## Writing rules

- Use simple technical English.
- Describe what happened, not what kind of person someone is.
- Avoid product-specific language unless it is necessary evidence supplied by the user.
- Keep ratings and examples grounded in the evidence. Do not calculate scores from output quality alone.
- Escape or remove secrets before creating the JSON.
