# Mode: followup — Follow-up Cadence

Check which applications are due for follow-up and draft the outreach.

## Trigger

User says: `/followup`, "what needs following up", "check my pipeline", "any overdue?"

## Cadence Rules

| Application Status | First Follow-up | Subsequent |
|--------------------|-----------------|------------|
| Applied            | After 7 days    | Once more at 14 days, then cold |
| Responded          | Within 1 day    | Every 3 days |
| Interview scheduled | Thank-you within 24h | Check-in every 3 days if no feedback |
| Post-interview     | Within 1 day    | Every 3 days up to 2 more times |

Applications with 2+ unanswered follow-ups are marked **cold**.

## Step 1 — Parse Applications

Read `career-ops/data/applications.md`. For each non-terminal row (not Offer/Rejected/Discarded/Cold):
- Calculate days since last action.
- Classify: `urgent` (overdue), `due` (due today), `waiting` (not yet due), `cold`.

## Step 2 — Dashboard

Display prioritized table:

```
FOLLOW-UP DASHBOARD — [Today's Date]
─────────────────────────────────────────────────────
 #   Company             Role              Status      Days  Action
─────────────────────────────────────────────────────
 !   Acme Corp           Staff Engineer    Applied     9d    OVERDUE — Draft follow-up
 !   Beta Inc            Senior SWE        Interview   2d    Thank-you due
     Gamma Ltd           EM                Applied     4d    Wait 3 more days
```

## Step 3 — Draft Follow-ups

For each urgent/due item, draft a follow-up email.

**First follow-up (Applied → 7+ days):**
- 3–4 sentences.
- Open with a specific reference to the role and one concrete value proposition from the evaluation report.
- Ask about timeline and next steps.
- Never "just checking in."

**Thank-you (post-interview, within 24h):**
- 4–5 sentences.
- Reference one specific topic discussed.
- Reiterate fit with one evidence point.
- Express genuine enthusiasm without desperation.

**Second attempt (14+ days, still no response):**
- 2–3 sentences. Different angle from first follow-up.
- If still no response after this, mark cold.

## Step 4 — Gmail Draft

For each approved draft:
1. Search `gmail.search_threads` for existing threads with that company/recruiter.
2. If thread found, note the thread ID so user can reply in-thread.
3. Call `gmail.create_draft` with draft text.
4. Confirm with user before creating.

## Step 5 — Calendar Reminder

For "waiting" items, offer to set a calendar reminder:
- Call `calendar.create_event` with title "Follow up: [Company] [Role]" on the due date.

## Step 6 — Update Tracker

After user confirms a follow-up was sent, append to the notes column in `applications.md`.

## Rules

- Never auto-send. Drafts only.
- Never follow up more than twice on Applied status.
- Mark cold after 2 unanswered attempts; don't draft a third.
- Always pull talking points from the evaluation report, not generic statements.
