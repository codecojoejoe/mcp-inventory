# Mode: interview-prep — Interview Preparation

Prepare for an upcoming interview using the evaluation report, company data, and CV.

## Trigger

User says: `/interview-prep [company or report #]`, "prepare for interview at [company]", "I have an interview".

## Pre-flight

1. Read `career-ops/cv.md`.
2. Find the evaluation report in `career-ops/reports/`.
3. Call `indeed.get_company_data` for fresh company intelligence (ratings, culture, recent news).
4. Check `calendar.list_events` to find the interview event and confirm timing.

## Output Structure

### 1. Role Intelligence Brief

Summarise from the evaluation report:
- Top 3 things they're hiring for.
- Likely pain points this role solves.
- Company culture signals (from company data ratings).

### 2. Your Strongest Stories (STAR format)

For each of the top 3 JD requirements, produce a STAR story from `cv.md`:

```
Requirement: [from JD]
Situation:   [context from your background]
Task:        [what you were responsible for]
Action:      [what you specifically did]
Result:      [quantified outcome]
Reflection:  [what you learned / why it matters here]
```

### 3. Questions to Ask Them

5 thoughtful questions derived from:
- The JD (role-specific gaps, team structure, success metrics).
- Company data (areas with lower ratings that are worth understanding).
- The evaluation report's concerns section.

Never: "What does the company do?" or "What are the benefits?" — research first.

### 4. Salary Negotiation Prep

If compensation scored < 4 in the evaluation:
- State your target number (from `_profile.md > ## Compensation`).
- Prepare one anchor sentence: "Based on my [X years / Y impact], I'm targeting [range]."
- Call `indeed.get_company_data` with job title to get salary benchmarks.

### 5. Logistics Checklist

- Confirm interview time from calendar.
- Confirm format (video/phone/onsite).
- If video: confirm link is in calendar event.
- If onsite: confirm address and travel time.

## Rules

- Ground every story in actual CV content — never fabricate.
- If interview is < 24h away, flag urgency and prioritise the stories section.
- Offer to update calendar event with prep notes.
