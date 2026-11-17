# Job 06 — Version history

**Task:** PLAN.md B10
**Route:** `/datasets/checkpd/versions/`
**File:** `src/pages/datasets/checkpd/versions/index.astro`

Read [00-README.md](00-README.md) first. This is the smallest job.

---

## Goal

The record of what changed between releases, and the statement of the versioning
rules the portal commits to. Version instability is a named project risk: changing
a file structure after publication breaks every analysis built on it.

## Page content

**Version table.** Columns: version, release date, status, DOI, main changes.

| Version | Release date | Status | DOI | Main changes |
|---|---|---|---|---|
| 2.0 | Pending | In preparation | Pending | Expanded cohort to 1,382; added `clinical_scores.csv`; added dual-tap and pinch-to-size; added `encode_*` columns; added `clinical_scores_available` and `dataset_version` |
| 1.0 | Unknown | Superseded | None | Initial release |

Take the v2.0 change list from the "Changes since v1.0" section that
`06-build-metadata.py` generates into `DATA_RELEASE/README.md` — that is the
generated source of truth. Take the cohort total from `summary.cohort.total`.

**v1.0's release date is not recorded anywhere in this repository.** Render
`Unknown`, not a guess. If you find it in `CheckPD_v1.0/README.md`, use it and
note where it came from.

**Versioning rules**, stated as commitments:

- Old versions are never overwritten or removed.
- Each release has a fixed file structure, frozen at publication.
- Each release has release notes.
- Publications must state the version used.
- Downloads are logged against the version downloaded.
- Each major version receives its own DOI; minor updates share it with version notes.
- Changes between versions are documented here.

**URL scheme.** Show the pattern and say that each version keeps a permanent URL:

```
/datasets/checkpd/v1.0/
/datasets/checkpd/v2.0/      ← current
/datasets/checkpd/v2.1/      future
```

State that `/datasets/checkpd/v2.0/` is the DOI resolution target and will not
move. v1.0 has no landing page yet — link only what exists.

**What counts as a new version.** Worth spelling out so future curators are
consistent: a major version for cohort or structure changes, a minor version for
metadata corrections that do not change the file structure.

## Acceptance

Beyond the shared checklist in [00-README.md](00-README.md):

- [ ] v2.0 change list matches the generated `DATA_RELEASE/README.md`.
- [ ] Cohort total comes from `summary.json`.
- [ ] No invented date or DOI; unknowns render as `Unknown` / `Pending`.
- [ ] No dead link to a v1.0 landing page that does not exist.
- [ ] Linked from the landing page and from `/datasets/`.
