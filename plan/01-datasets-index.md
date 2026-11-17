# Job 01 — Dataset index

**Task:** PLAN.md B5
**Route:** `/datasets/`
**File:** `src/pages/datasets/index.astro`

Read [00-README.md](00-README.md) first.

---

## Goal

The list of datasets this portal publishes. Today that is CheckPD v2.0, with v1.0
noted as superseded. It must read as a repository index, not a single product
page — the portal is meant to carry CheckBrain, CheckSleep and future releases.

Someone lands here from the main nav or from a search result. They need to know
within one screen: what datasets exist, how big they are, what access level they
carry, and where to go next.

## Page content

**Header.** `.eyebrow` "Datasets", h1 "Datasets", a one-paragraph `.lede`
explaining that releases are versioned, frozen, and citable, and that older
versions stay available.

**Current release card.** CheckPD v2.0. Include:

- Title from `dataset.title`, linked to `dataset.path`
- `badge--brand` with `dataset.accessLevel`, plus a `badge` with the version
- Cohort line from `summary.cohort` — total, PD, HC
- Modality count and `summary.release.total_files` / `total_bytes`
- Short description from `dataset.tagline`
- A "View dataset" link to `dataset.path`

Use `StatTiles` if it reads better than inline text, but keep this card lighter
than the landing page — this is an index, not a duplicate of `/datasets/checkpd/v2.0/`.

**Superseded releases.** A row for CheckPD v1.0: superseded by v2.0, retained for
reproducibility, no landing page yet. Do not invent counts for it — we have not
derived them. Say "see the v2.0 release notes" or leave the figures out.

**Forthcoming.** One short paragraph naming the planned series (CheckBrain,
CheckSleep, and longitudinal CheckPD follow-up) as future work, with no dates.
Keep it clearly labelled as planned, not available.

**Versioning note.** A `.note` stating: releases are frozen, never overwritten;
each major version gets its own DOI; publications must state the version used.
Link to `/datasets/checkpd/versions/` (job 06).

## Constraints specific to this job

- v1.0 figures are not in `summary.json` and must not be guessed.
- Do not describe v2.0 as released — `dataset.status` is `in-preparation`. Reuse
  the same "In preparation" badge treatment as the landing page.

## Acceptance

Beyond the shared checklist in [00-README.md](00-README.md):

- [ ] Every CheckPD v2.0 figure traces to `summary.json`.
- [ ] No figure is stated for v1.0.
- [ ] Page reads as a list that can grow, not as a single-dataset page.
- [ ] Header nav shows `/datasets/` as current.
