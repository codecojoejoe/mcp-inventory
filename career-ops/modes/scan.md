# Mode: scan — Job Discovery

Discover new job postings and add qualified ones to `career-ops/data/pipeline.md`.

## Trigger

User says: `/scan`, "scan for jobs", "find new openings", or similar.

## Pre-flight

1. Read `career-ops/cv.md` and `career-ops/_profile.md` to load search context.
2. Read `career-ops/data/scan-history.tsv` to know what's already been seen.
3. Read `career-ops/data/applications.md` to avoid re-adding applied roles.

## Search Strategy

Run all three levels in parallel for speed.

### Level 1 — Indeed (primary)

Call `indeed.search_jobs` with:
- `search`: each target role from `_profile.md > ## Target Roles`
- `location`: each preferred location from `_profile.md > ## Locations`
- `country_code`: from profile
- `job_type`: "fulltime" unless profile says otherwise

### Level 2 — LinkedIn (complementary)

Call `linkedin_jobs.search_jobs` with:
- `keyword`: same role titles
- `location`: same locations
- `workplace_types`: per profile preference (e.g. `["Remote", "Hybrid"]`)
- `posted_date`: "SEVEN" to catch the last 7 days
- `employment_types`: `["FULL_TIME"]`

### Level 3 — Targeted company search

For each company in `_profile.md > ## Target Companies`, run:
- `indeed.search_jobs` with `search: "[role] at [company]"`
- `indeed.get_company_data` if not yet profiled

## Filtering

**Include** if job title matches any positive keyword in `_profile.md > ## Title Keywords`.
**Exclude** if title matches any negative keyword (e.g. "intern", "junior" if seniority is senior).
**Exclude** if job ID / URL already appears in `scan-history.tsv` or `applications.md`.

## Output

For each new qualifying job, append to `career-ops/data/pipeline.md`:

```
- [ ] [Company] | [Title] | [Location] | [Source: Indeed/LinkedIn] | [Job ID or URL] | [Salary if shown]
```

Then append to `scan-history.tsv`:
```
[ISO date]\t[job_id]\t[company]\t[title]\t[source]\tadded
```

Finish with a summary table:

| Source | Found | Filtered | Duplicates | Added to pipeline |
|--------|-------|----------|------------|-------------------|
| Indeed | N     | N        | N          | N                 |
| LinkedIn | N   | N        | N          | N                 |

## Rules

- Never modify `cv.md` or `_profile.md`.
- Never add jobs with score < 3.0 from a quick title-only filter.
- If `_profile.md` is empty, ask the user to fill it before scanning.
