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
- `employment_types`: ["FULL_TIME"]
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

```
site:gem.com "[role]" remote
```
Also try:
```
site:boards.gem.com "[role]"
```
Verify liveness before adding.

### Channel 6 — Direct Company Career Pages (targeted)

For each company in `_profile.md > ## Target Companies`, search:
```
site:[company].com/careers "[role]"
```
Or use known ATS URL if available (e.g. company uses Greenhouse — use boards.greenhouse.io/[company]).

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
