# Career-Ops

AI-powered job search and application pipeline built on Claude Code.

**Source of truth files — read before every operation:**
- `career-ops/cv.md` — your CV (fill this in first)
- `career-ops/_profile.md` — target roles, locations, compensation, north star

**Data files — updated automatically:**
- `career-ops/data/pipeline.md` — job queue for evaluation
- `career-ops/data/applications.md` — application tracker
- `career-ops/data/scan-history.tsv` — deduplication log
- `career-ops/reports/` — evaluation reports (one per job)

---

## Slash Commands

| Command | What it does |
|---------|-------------|
| `/scan` | Search Indeed + LinkedIn for new jobs matching your profile |
| `/pipeline` | Evaluate all pending jobs in the queue |
| `/evaluate [job]` | Evaluate a single job (URL, ID, or pasted JD) |
| `/apply [report #]` | Draft cover letter + Gmail draft for a specific job |
| `/followup` | Check which applications are overdue for follow-up |
| `/tracker` | Display and update the full application dashboard |
| `/interview-prep [company]` | Prepare for an upcoming interview |

---

## Workflow

```
/scan           →  new jobs added to pipeline.md
/pipeline       →  each job scored A–F, reports saved
/apply [#]      →  cover letter drafted, Gmail draft created (you send)
/followup       →  follow-up emails drafted at right cadence (you send)
/tracker        →  update status as recruiter responses come in
/interview-prep →  STAR stories + company intel before the call
```

---

## MCP Tools Available

| MCP | Tools Used For |
|-----|---------------|
| **Indeed** | Job search, job details, company ratings/salaries |
| **LinkedIn Jobs** | Complementary job search with workplace type filters |
| **Gmail** | Draft cover letters, follow-ups, thank-you notes |
| **Google Calendar** | Schedule interviews, set follow-up reminders |
| **Google Drive** | Store resume versions, retrieve templates |

---

## Core Rules

1. **Never auto-send email.** Create drafts only. Human clicks send.
2. **Never auto-submit applications.** Human reviews and submits.
3. **Never invent CV content.** Ground every claim in `cv.md`.
4. **Always read cv.md + _profile.md** before any scan, evaluation, or application.
5. **Warn before applying to jobs scoring < 3.5.**
6. **Deduplication:** check scan-history.tsv and applications.md before adding to pipeline.

---

## Setup Checklist

- [ ] Fill in `career-ops/cv.md` with your actual experience
- [ ] Fill in `career-ops/_profile.md` with target roles, locations, compensation
- [ ] Run `/scan` to discover your first batch of jobs
- [ ] Run `/pipeline` to evaluate them
- [ ] Run `/apply` on the best ones

---

## Scoring Reference

| Score | Band | Action |
|-------|------|--------|
| 4.5+ | Excellent | Apply immediately |
| 4.0–4.4 | Strong | Worth applying |
| 3.5–3.9 | Marginal | Apply if motivated |
| < 3.5 | Weak | Recommend against |
