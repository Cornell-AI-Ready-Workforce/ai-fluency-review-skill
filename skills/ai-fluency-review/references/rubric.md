# AI fluency rubric

## Constructs

Assess behavior, not personality.

| Area | Meaning |
|---|---|
| Description | Give AI a clear goal, useful context, limits, and audience. |
| Delegation | Choose what AI should do, what the person should keep, and who checks the result. |
| Discernment | Question AI output and identify weak, missing, or unsupported claims. |
| Diligence | Check sources, protect information, test results, and finish the work carefully. |
| Adaptive Flexibility | Use feedback, change the approach, verify the change, and carry the lesson forward. |

## Five behavior labels

Use whole labels only. Do not display decimals or percentages.

| Level | Label | General anchor |
|---|---|---|
| 1 | Rarely observed | The behavior is rarely visible in the available evidence. |
| 2 | Emerging | The behavior appears with prompting or in simple cases but is inconsistent. |
| 3 | Usually observed | The behavior is usually present in clear tasks but weakens in complex or sustained work. |
| 4 | Consistent across contexts | The behavior is consistent across varied tasks and includes useful checks or boundaries. |
| 5 | Consistent and reusable | The behavior is consistent, anticipates failure, and becomes a reusable practice for future work. |

Use `null` when evidence is too sparse, contradictory, or uneven to support a label.

## Area-specific anchors

### Description

- 1: Requests are vague and omit the desired outcome.
- 2: States a goal but often omits context, limits, audience, or completion criteria.
- 3: Usually supplies the goal and useful context; complex requests may remain broad.
- 4: Defines outcomes, constraints, evidence, risks, and what finished work looks like.
- 5: Adapts briefs to audience and risk, anticipates ambiguity, and reuses effective request patterns.

### Delegation

- 1: Gives AI broad control without choosing responsibilities or review points.
- 2: Chooses some tasks for AI but ownership and approval remain unclear.
- 3: Usually separates AI work from human decisions; coordination can weaken across many tasks.
- 4: Assigns clear roles, boundaries, owners, reviewers, and handoffs.
- 5: Designs reliable multi-step collaboration with explicit authority, escalation, and reusable delegation rules.

### Discernment

- 1: Accepts unsupported output or misses obvious contradictions.
- 2: Questions output after a problem appears but checks are inconsistent.
- 3: Usually checks important claims and notices weak evidence.
- 4: Defines rejection criteria, tests assumptions, and seeks independent support before relying on output.
- 5: Calibrates trust to risk, anticipates failure modes, and uses repeatable evaluation methods.

### Diligence

- 1: Important work is left unchecked, unsafe, or unfinished.
- 2: Performs some checks but misses sources, privacy, testing, or durable closure.
- 3: Usually checks and completes work; complex or parallel work may end without saved proof or handoff.
- 4: Verifies sources and results, protects sensitive information, and closes with durable evidence.
- 5: Uses repeatable quality gates, provenance, recovery paths, and clear completion records across workstreams.

### Adaptive Flexibility

- 1: Repeats failures without changing the approach.
- 2: Notices friction or responds after prompting but the change is temporary.
- 3: Fixes the current task and can explain what went wrong.
- 4: Changes the workflow, verifies the change, and applies the lesson to later work.
- 5: Maintains a reusable learning loop that records failures, rules, tests, and results across contexts.

## Evidence rules

1. Use dated, observable behavior. Prefer direct requests, corrections, checks, decisions, and saved artifacts.
2. Keep one or two strongest examples per area. More examples do not automatically increase a score.
3. Identify evidence with a date, short task context, and observed action. Add a stable user-visible source link when possible; never show an opaque identifier without context.
4. Record observed counterevidence. Label missing behavior or unavailable sources as an evidence gap, not counterevidence. Absence of evidence can reduce confidence or leave a higher label unsupported, but it is not proof of poor behavior.
5. Distinguish the person's choices from actions automatically performed by the AI or harness.
6. Compare periods only when both have enough relevant evidence. State material coverage differences.
7. Treat a caught mistake as positive evidence of discernment. Evaluate Adaptive Flexibility by what changed afterward.
8. Do not infer intelligence, motivation, employability, mental state, or other traits.
9. Do not turn unequal period lengths into a rate claim. Do not invent missing date components.
10. An artifact open or click shows exposure only. It is not proof that the person read, understood, evaluated, or authored anything.
11. Agent-only actions never increase the person's rating. Events with an unknown actor cannot support Levels 4 or 5.
12. Credit an edit only when provenance identifies the human contribution. For a mixed edit, credit only the attributable human action, such as setting a constraint, revising text, accepting a change, or rejecting output.
13. Prefer event sequences to isolated events. A sequence such as open, inspect, revise, decide, and reuse supports a stronger inference than any one click.
14. Level 4 requires supporting behavior in at least two distinct contexts; with only one context, cap the rating at Level 3. Level 5 requires at least three contexts, high-confidence human provenance, and no unresolved material counterevidence.
15. Report provenance counts only from explicit event-level records. Narrative summaries can support behavior ratings, but not precise actor or interaction totals.
16. Broad inventory is the default. Choose the evidence unit that matches the source, such as a conversation, task, run, activity segment, or work episode, then inventory every accessible direct unit in each comparison window before rating. Deep-read all when feasible; otherwise use a reproducible neutral sample across active dates and varied contexts, disclose the unit, rule, and counts, and never choose only the strongest episodes. If full inventory is impossible, state the access limit and do not call the sample representative.
17. Level 4 requires the behavior to dominate relevant opportunities across contexts. Explain why any material counterexamples do not defeat the consistency claim. Use judgment rather than a numeric threshold.

## Interaction provenance

Record relevant events with four separate fields:

- **Action:** what occurred, such as opening an artifact, following a source, clicking an action, editing, commenting, approving, rejecting, rerunning, downloading, or sharing.
- **Actor:** `human`, `agent`, `mixed`, or `unknown`.
- **Attribution basis:** how authorship was determined, such as explicit authorship, tracked change, event origin, session attribution, inference, or unknown.
- **Provenance confidence:** `high`, `medium`, or `low`.

Use tracked changes or diffs when available. Do not infer that the human made an edit merely because the edit appeared during a human-owned session.

## Evidence strength labels

- **High:** relevant behavior is repeated across contexts, most scored evidence has high-confidence human attribution, and important counterevidence and coverage gaps were checked.
- **Medium:** useful evidence exists, but context count, attribution, comparison windows, or counterevidence is incomplete.
- **Low:** evidence is sparse, mostly agent-only or unknown, materially uneven, or too ambiguous for a stable interpretation.

Area and period evidence strength describe evidence quality, not skill level. A Level 4 result can still have Low evidence strength and should then be treated as provisional.

## Use with candidates or employees

This review may summarize consented, job-relevant observed behavior for a human reviewer. It must not automatically rank people, infer employability, or decide hiring, promotion, pay, or discipline. Disclose the event categories collected, who can access them, and how long they are retained. Never interpret clicks as hidden measures of effort, attention, or intent.

## Adaptive Flexibility change over time

Current-task adaptation can support Levels 2 or 3 without proving change over time. Levels 4 and 5 require later reuse as stated in their anchors. Describe change over time only when the evidence shows all four links: feedback or friction, a changed approach, a checked result, and reuse in a later task. Use the current Adaptive Flexibility rating from the five-area snapshot; do not create a second current score in the change section. A comparable earlier-period rating is optional. If the chain or period comparability is incomplete, state: “Not enough evidence to evaluate change over time.” Do not manufacture intermediate time points.
