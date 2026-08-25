# Assessment record v0.2

Use this optional private JSON record when a reproducible report or audit trail is useful. The agent may create the HTML directly without it.

Validate records against [../assets/assessment-record.schema.json](../assets/assessment-record.schema.json). Start from [../assets/assessment-template.json](../assets/assessment-template.json).

## Top-level fields

- `schema_version`, `rubric_version`, `renderer_version`: explicit contract versions.
- `meta`: title, generated date, review period, and participant-facing coverage line.
- `evidence_inventory`: evidence unit, source types, periods, counts, sampling method, access limits, and attribution limits.
- `reliability`: overall `evidence_strength` plus material limitations.
- `standouts`: strongest observed habit, current focus, and one action to try next.
- `areas`: exactly one record for each of the five required ids.
- `adaptive_flexibility_change`: longitudinal conclusion without duplicating the current Adaptive Flexibility rating.
- `interaction_events`: optional private provenance records. These are never copied into the HTML.

## Area records

Required ids are `description`, `delegation`, `discernment`, `diligence`, and `adaptive-flexibility`.

Each area contains:

- `display_label`: the action label shown prominently to participants.
- `research_label`: the 4D or longitudinal construct name.
- `level`: integer 1–5 or `null`.
- `evidence_strength`: `low`, `medium`, or `high`.
- `observed_pattern`, `inconsistent_patterns`, and `evidence_gaps`.
- `opportunities_to_observe`, `contexts_observed`, and `rating_rationale` for auditability.
- `recommended_action`: one small action to try on a new task.
- `evidence`: zero to two concise examples.

An evidence example separates participant-facing and private source information:

```json
{
  "date": "2026-08-18",
  "task_label": "Policy summary",
  "summary": "You checked a conflicting number against the source before using it.",
  "source_label": "Policy source check",
  "source_url": null,
  "private_source_id": "episode-004"
}
```

The renderer omits `private_source_id`. It includes `source_url` only when present and safe to expose.

## Change over time

`adaptive_flexibility_change.status` is either `supported` or `not-enough-evidence`. A supported conclusion records the friction, changed approach, verified result, and later reuse. The current rating remains canonical in `areas`; the change object must not repeat it.

## Interaction provenance

Optional `interaction_events` use the actions `request`, `delegate`, `inspect`, `verify`, `revise`, `decide`, `reuse_practice`, or `other`. Record actor, attribution basis, and provenance strength separately. An open or click may be recorded as `inspect` only when the evidence shows inspection; otherwise omit it or use `other` without inferring judgment.

## Privacy

- Keep assessment JSON private; it may contain detailed activity references.
- Keep secrets, raw transcripts, and unnecessary personal data out of the record.
- Do not infer human authorship from session ownership.
- Do not use the record for automated ranking or employment decisions.
