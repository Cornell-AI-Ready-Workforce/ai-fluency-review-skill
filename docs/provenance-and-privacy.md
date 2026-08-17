# Provenance and privacy

## Event provenance

Relevant interaction events may include artifact opens, source opens, action clicks, edits, comments, approvals, rejections, reruns, downloads, and shares.

Every event separates:

- action: what occurred;
- actor: human, agent, mixed, or unknown;
- attribution basis: how the actor was established;
- provenance confidence: high, medium, or low;
- artifact and time identifiers;
- an optional source or diff reference.

Do not infer human authorship merely because an edit occurred during a human-owned session. Mixed work should identify the attributable human contribution without crediting the agent's work to the person.

## Data minimization

Collect only task-relevant events that the person has been informed about. Avoid raw keystrokes, unrelated browsing, message contents, or background activity when a smaller event record is sufficient.

The HTML receives aggregate counts and concise conclusions only. Raw source references, event summaries, and diffs stay in the assessment JSON. Treat that JSON as a restricted audit artifact.

## Evaluated people

For candidates, employees, students, or other evaluated people:

- disclose the event categories collected;
- state who can access the records and how long they are retained;
- allow correction of misattributed actions;
- keep a human reviewer responsible for interpretation;
- do not infer effort, attention, motivation, intelligence, or employability from clicks;
- do not automate ranking or consequential decisions.
