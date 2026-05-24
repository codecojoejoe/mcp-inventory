# Mode: evaluate — Job Opportunity Scoring

Score a single job posting A–F across six dimensions and produce a structured report.

## Trigger

User says: `/evaluate [job URL or ID]`, "evaluate this job", pastes a job description, or `/pipeline` processes a pending item.

## Pre-flight

1. Read `career-ops/cv.md` — required. Never evaluate without it.
2. Read `career-ops/_profile.md` — required for North Star alignment.
3. Fetch job details:
   - If a job ID is provided: call `indeed.get_job_details(job_id)`.
   - If a URL is provided: use WebFetch.
   - If text is pasted: use it directly.

## Scoring Rubric (1–5 per dimension)

### A — CV Match
How well does the JD align with the candidate's demonstrated skills and experience?
- 5: 80%+ of required skills are on the CV with direct experience.
- 4: 60–79% match; minor gaps closable quickly.
- 3: 40–59% match; significant ramp-up needed.
- 2: <40% match or major missing requirements.
- 1: Fundamental mismatch.

### B — North Star Alignment
Does the role advance the candidate's stated career direction from `_profile.md`?
- 5: Exact archetype match (title, industry, growth trajectory).
- 4: Strong overlap; one dimension off.
- 3: Partial; role is acceptable but not ideal direction.
- 2: Sideways move; unlikely to advance stated goals.
- 1: Counter to career direction.

### C — Compensation
How does stated/implied compensation compare to target range in `_profile.md`?
- 5: Meets or exceeds target; top-quartile market rate.
- 4: Within 10% of target.
- 3: 10–20% below target but negotiable.
- 2: 20–30% below or no salary info at all.
- 1: Clearly below market or explicitly low.

### D — Cultural Signals
Company stability, growth trajectory, remote/hybrid policy, team size signals.
- 5: Strong positive signals across all dimensions.
- 4: Mostly positive; minor concerns.
- 3: Mixed; some positives offset by unknowns.
- 2: Notable concerns (recent layoffs, vague remote policy, etc.).
- 1: Significant red flags.

Use `indeed.get_company_data` to pull ratings, CEO approval, work-life balance scores.

### E — Red Flags
Active blockers or serious warnings.
- 5: None detected.
- 4: Minor concerns only.
- 3: One moderate concern.
- 2: Multiple concerns or one serious one.
- 1: Hard blocker (requires relocation when remote-only desired, requires clearance, etc.).

### F — Global Score
Weighted average: A×0.30 + B×0.20 + C×0.20 + D×0.15 + E×0.15

## Score Bands
| Score | Action |
|-------|--------|
| 4.5+  | Apply immediately |
| 4.0–4.4 | Worth applying |
| 3.5–3.9 | Apply if motivated |
| < 3.5 | Recommend against |

## Legitimacy Check

Separate from score. Flag any of:
- Posted > 30 days ago
- No apply button or broken link
- Vague JD (< 200 words, no specific requirements)
- Salary range missing
- Role reposted multiple times

## Report Format

Save to `career-ops/reports/[NNN]-[Company]-[Role].md` where NNN is next sequential number.

```markdown
# [NNN] [Company] — [Role]
**Date:** YYYY-MM-DD  
**Source:** Indeed / LinkedIn / Direct  
**Apply URL:** [link]

## Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| A — CV Match | X/5 | ... |
| B — North Star | X/5 | ... |
| C — Compensation | X/5 | ... |
| D — Culture | X/5 | ... |
| E — Red Flags | X/5 | ... |
| **F — Global** | **X.X/5** | |

**Band:** Apply immediately / Worth applying / Apply if motivated / Against

## Legitimacy
[Signals found. Constructive framing.]

## Key Strengths
- ...

## Concerns
- ...

## Suggested Talking Points
- ...

## Cover Letter Draft
[See apply mode or auto-draft here]
```

## After Evaluating

Update `career-ops/data/pipeline.md`: mark item `[x]` and add score.
Update `career-ops/data/applications.md` if user decides to apply.

## Rules

- Never invent scores — cite exact CV lines and JD requirements.
- Never auto-submit anything.
- Always include the apply URL in the report.
- If CV is empty/placeholder, ask user to fill it before scoring.
