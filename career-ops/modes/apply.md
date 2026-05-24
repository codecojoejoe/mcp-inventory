# Mode: apply — Application Assistant

Draft cover letter, customise resume talking points, and create a Gmail draft ready to send.

## Trigger

User says: `/apply [report number or company]`, "apply to this", "draft cover letter for [role]".

## Pre-flight

1. Read `career-ops/cv.md`.
2. Read `career-ops/_profile.md` for writing style calibration.
3. Find the relevant evaluation report in `career-ops/reports/`.
   - If no report exists, run evaluate mode first. Ask user to confirm before proceeding.

## Step 1 — Cover Letter

Write a cover letter following these rules:

**Structure:**
1. Opening hook — one specific thing about the company or role that genuinely interests the candidate. No clichés ("I am passionate about...").
2. Why you — 2–3 sentences connecting the most relevant CV experience directly to the top JD requirements. Cite real numbers/outcomes.
3. Why them — one sentence on why this company specifically, drawn from company data or the JD.
4. Call to action — brief, confident close.

**Tone calibration:**
- Match the writing style extracted in `_profile.md > ## Writing Style`.
- If no style captured yet, infer from cv.md narrative sections.
- Avoid: "leverage", "synergies", "passionate", "dynamic", "results-driven".
- Target: specific, direct, warm, evidence-based.

**Length:** 250–350 words. Never longer.

## Step 2 — Resume Talking Points

List 5–7 bullet points to highlight in the application form or interview:
- Each maps a JD requirement to a specific CV achievement.
- Format: `[JD Requirement] → [Your Evidence]`

## Step 3 — Gmail Draft

Call `gmail.create_draft` with:
- `to`: recruiter email if known (from JD or LinkedIn); otherwise leave blank.
- `subject`: "Application — [Role] at [Company]"
- `body`: the cover letter above, formatted as plain text email.

Confirm with user before creating the draft.

## Step 4 — Update Tracker

After user confirms they're applying, update `career-ops/data/applications.md`:
- Add new row with status "Applied".
- Record date, company, role, score, and report number.

## Step 5 — Google Drive (optional)

If user has a resume file in Drive, call `drive.search_files` for their master resume,
then `drive.copy_file` to create `Resume - [Company] - [Role] - [YYYY-MM-DD]` as a saved record.

## Rules

- Never send the email — only create a draft. Human sends.
- Never fabricate experience not in `cv.md`.
- If score < 3.5, warn user before proceeding: "This role scored X/5. Do you still want to apply?"
- Always confirm draft content with user before calling `gmail.create_draft`.
