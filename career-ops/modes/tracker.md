# Mode: tracker — Application Status Dashboard

Display, update, and analyse the full application pipeline.

## Trigger

User says: `/tracker`, "show my applications", "update status", "how many applications", "pipeline stats".

## Data Source

All data lives in `career-ops/data/applications.md`.

## Status Flow

```
Evaluating → Applied → Responded → Phone Screen → Interview → Final Round → Offer / Rejected
                                                                          ↘ Discarded (user withdrew)
                                                          ↘ Cold (no response after 2 follow-ups)
```

## Display Format

Show the full table, then stats:

```
APPLICATION TRACKER — [Today's Date]
═══════════════════════════════════════════════════════════════════════
 #    Date        Company          Role                Score  Status        Report
───────────────────────────────────────────────────────────────────────
 001  2026-05-20  Acme Corp        Staff Engineer      4.2    Applied       reports/001
 002  2026-05-21  Beta Inc         Senior SWE          4.7    Interview     reports/002
───────────────────────────────────────────────────────────────────────

STATS
 Total applications : 2
 Active             : 2
 Interviews         : 1
 Offers             : 0
 Rejected           : 0
 Cold               : 0
 Average score      : 4.45
 Response rate      : 50%
```

## Updating Status

When user says "update [company] to [status]" or "mark [#] as [status]":
1. Find the row in `applications.md`.
2. Update the status column.
3. If status is "Interview", offer to create a calendar event via `calendar.create_event`.
4. If status is "Offer", congratulate and ask if they want to draft a negotiation email.
5. Confirm change with user before writing.

## Filtering

Support: "show only interviews", "show active", "show this week", "show score > 4.0".

## Rules

- Never delete rows — use "Discarded" status instead.
- Never auto-update without user confirmation.
- If user asks for a report, pull the corresponding file from `career-ops/reports/`.
