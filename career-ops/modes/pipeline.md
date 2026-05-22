# Mode: pipeline — Process Pending Jobs

Evaluate all pending items in `career-ops/data/pipeline.md` in sequence (or parallel for 3+).

## Trigger

User says: `/pipeline`, "process my pipeline", "evaluate all pending", "work through the queue".

## Step 1 — Load Queue

Read `career-ops/data/pipeline.md`. Count items marked `- [ ]`.

If queue is empty, say so and suggest running `/scan` to discover new jobs.

## Step 2 — Process Each Item

For each `- [ ]` item:

1. Extract company, role, source, and job ID / URL.
2. Run the full evaluate mode logic (see `modes/evaluate.md`).
3. Save report to `career-ops/reports/`.
4. Mark item `[x]` in pipeline with score.

For 3+ items: process in parallel batches of 3.

## Step 3 — Summary Table

After processing all items:

```
PIPELINE RESULTS — [Date]
─────────────────────────────────────────────────────────
 #    Company          Role               Score   Band              Report
─────────────────────────────────────────────────────────
 001  Acme Corp        Staff Engineer     4.2     Worth applying    reports/001
 002  Beta Inc         Senior SWE         4.8     Apply immediately reports/002
 003  Gamma Ltd        EM                 3.1     Against           reports/003
─────────────────────────────────────────────────────────
 Evaluated: 3  |  Apply immediately: 1  |  Worth applying: 1  |  Against: 1
```

## Step 4 — Apply Prompt

For each item scoring 4.0+, ask:
"Would you like me to draft an application for [Company] — [Role] (score: X.X)?"

If yes, run apply mode.

## Rules

- Never auto-apply. Always ask first.
- Never skip the evaluate pre-flight (cv.md + _profile.md).
- If a job URL is inaccessible, mark `[!]` with an error note and continue.
- Pause after 5 evaluations to avoid overloading context; ask if user wants to continue.
