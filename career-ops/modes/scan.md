# Mode: scan — Job Discovery

Discover new job postings and add qualified ones to `career-ops/data/pipeline.md`.

## Trigger

User says: `/scan`, "scan for jobs", "find new openings", or similar.

## Pre-flight

1. Read `career-ops/cv.md` and `career-ops/_profile.md` to load search context.
2. Read `career-ops/data/scan-history.tsv` to know what's already been seen.
3. Read `career-ops/data/applications.md` to avoid re-adding active roles.

## Sourcing Rules

**Use:** LinkedIn, Greenhouse, Lever, Ashby, GEM — ATS-direct only.
**Never use:** Indeed, Dice, Lensa, or any aggregator.

---

## Search Channels

Run all channels in parallel.

### Channel 1 — LinkedIn (MCP)

Call `linkedin_jobs.search_jobs` for each target role:
- `keyword`: each title from `_profile.md > ## Target Roles` (Primary first)
- `location`: "remote" or "United States"
- `workplace_types`: ["Remote"]
- `employment_types`: ["FULLTIME"]
- `posted_date`: "SEVEN"

Also run a second pass excluding Senior-only results by appending "staff OR principal" to keyword.

### Channel 2 — Greenhouse (WebSearch)

For each target role title, run:
```
site:boards.greenhouse.io "[role]" remote
```
Fallback:
```
site:boards.greenhouse.io "[role]"
```
Verify each result is live (non-redirect, apply button present) before adding.

### Channel 3 — Lever (WebSearch)

```
site:jobs.lever.co "[role]" remote
```
Lever URLs follow pattern: `jobs.lever.co/[company]/[job-id]`
Verify liveness before adding.

### Channel 4 — Ashby (WebSearch)

```
site:jobs.ashbyhq.com "[role]" remote
```
Verify liveness before adding.

### Channel 5 — GEM (WebSearch)

GEM format is `jobs.gem.com/[company]` — not a general index. Only scan if you know the company's GEM URL.

For each known GEM company (add to `_profile.md > ## GEM Companies`):
```
site:jobs.gem.com/[company] "[role]"
```
Verify liveness before adding.

### Channel 6 — Workday (WebSearch)

Many enterprise tech, fintech, and healthtech companies run on Workday ATS. Broad coverage with:
```
site:myworkdayjobs.com "staff" "identity" OR "IAM" remote
site:myworkdayjobs.com "staff systems engineer" "identity"
site:myworkdayjobs.com "principal" "IAM" OR "identity" remote
```
Also targeted per company:
```
site:myworkdayjobs.com/[company] "[role]"
```
Note: Workday URLs contain dynamic job IDs. Verify each listing is live via WebFetch before adding.

### Channel 8 — Wellfound / AngelList (WebSearch)

Strong for AI startups and early-stage companies. Two approaches:

**Broad search** (individual job postings have URLs at `wellfound.com/jobs/[id]-[slug]`):
```
site:wellfound.com/jobs "identity" OR "IAM" "staff" remote
site:wellfound.com/jobs "IT engineer" OR "systems engineer" "staff" remote Okta
```
Note: Wellfound's public index is shallow — many listings don't surface. Company pages are more reliable.

**Targeted company pages** (check each target company from `_profile.md > ## Target Companies`):
```
wellfound.com/company/[company-slug]/jobs
```
Examples:
- `wellfound.com/company/anthropic/jobs`
- `wellfound.com/company/openai/jobs`
- `wellfound.com/company/elevenlabs/jobs`

WebFetch is blocked on Wellfound (requires login). Use WebSearch only.


### Channel 7 — Direct Company Career Pages (targeted)

For each company in `_profile.md > ## Target Companies`, search:
```
site:[company].com/careers "[role]"
```
Or use known ATS URL if available.

## Google Search Pattern Reference

Best-performing patterns (use verbatim in WebSearch):

```
site:jobs.lever.co "staff systems engineer" "identity"
site:jobs.lever.co "staff" "IAM" remote
site:boards.greenhouse.io "staff" "identity" "corporate" remote
site:boards.greenhouse.io "staff IAM engineer" remote
site:jobs.ashbyhq.com "staff IT engineer" remote
site:jobs.ashbyhq.com "staff corporate engineer" "identity"
site:myworkdayjobs.com "staff systems engineer" "identity"
site:myworkdayjobs.com "automation engineer" "AI" remote
```

Tip: Avoid `OR` chains in a single query — split into separate searches for better index coverage.

---

## Filtering Rules

**Include** if:
- Title contains a positive keyword from `_profile.md > ## Title Keywords (positive)`
- Role is explicitly remote or location-flexible
- Seniority matches (Staff, Principal, Senior Staff, or Manager)
- Company passes the profile's company quality bar

**Exclude** if:
- Title matches a negative keyword (intern, junior, associate, contract, product engineer, software engineer)
- Role is onsite or hybrid with mandatory office days
- Job ID / URL already in `scan-history.tsv` or `applications.md`
- Listing is dead (broken URL, no apply button, redirects to homepage)
- Contract or staffing agency posting

**Minimum per scan:** 5 net-new qualifying roles. Keep scanning until threshold is met.

---

## Output

For each qualifying new job, append to `career-ops/data/pipeline.md`:

```
- [ ] [Company] | [Title] | [Location/Remote] | [Source: LinkedIn/Greenhouse/Lever/Ashby/GEM/Direct] | [URL] | [Salary if shown]
```

Append to `career-ops/data/scan-history.tsv`:
```
[ISO date]\t[url_or_id]\t[company]\t[title]\t[source]\tadded
```

For filtered/dead listings, still log them as `filtered` or `dead` in scan-history to prevent re-checking.

---

## Summary Table

```
SCAN RESULTS — [Date]
──────────────────────────────────────────────────────────
 Channel     Found   Filtered   Dead   Duplicate   Added
──────────────────────────────────────────────────────────
 LinkedIn      N        N        N        N          N
 Greenhouse    N        N        N        N          N
 Lever         N        N        N        N          N
 Ashby         N        N        N        N          N
 GEM           N        N        N        N          N
 Direct        N        N        N        N          N
──────────────────────────────────────────────────────────
 Total         N        N        N        N          N
```

If fewer than 5 net-new roles were added, say so and explain why (thin market, all filtered, etc.).

---

## Rules

- Never use Indeed or any aggregator.
- Never add a listing without verifying it's live.
- Never add a role already in the active pipeline or applications tracker.
- Never modify `cv.md` or `_profile.md`.
- Minimum 5 net-new roles per scan run.
