# Job 05 — Citation

**Task:** PLAN.md B9
**Route:** `/datasets/checkpd/v2.0/citation/`
**File:** `src/pages/datasets/checkpd/v2.0/citation/index.astro`

Read [00-README.md](00-README.md) first.

---

## Goal

Make it impossible to cite this dataset wrongly. Citation fragmentation is a named
project risk: researchers cite the website instead of the versioned dataset, or
omit which version they used, and the work stops being reproducible.

## The DOI arrangement — get this right, it is the whole point of the page

Two DOIs will exist, and they mean different things. A reader must not confuse them.

**Zenodo — short term.** A record titled `dataset.doi.zenodoRecordTitle`
("CheckPD v2.0: Dataset Documentation and Access Record") holding the files listed
in `dataset.doi.zenodoContents`: README, data dictionary, questionnaire schema,
file manifest, validation summary, access protocol, and the public sample.

**It contains no participant data.** Say so explicitly and prominently. Someone
who finds the Zenodo record and expects the dataset must immediately understand
that the data itself is here, under credentialed access.

**DataCite — long term.** An institutional DOI resolving to this same landing page.

Both resolve to `/datasets/checkpd/v2.0/`. Because the target never changes,
anything already cited stays valid when DataCite replaces Zenodo as the primary.
State that too — it is the reason the arrangement is safe.

Render from `dataset.doi.zenodo` and `dataset.doi.datacite`, both `null` today.
Show `Pending` for each. `citations()` already emits `<DOI pending>`.

## Page content

**Citation formats** — Vancouver, APA and BibTeX, each in a bordered block with a
copy button. Reuse the `.cite` markup and `data-copy` pattern from the landing
page; the handler is already in `Base.astro`.

Build them with `citations(activeDoi)` from `dataset.ts`. Do not write citation
strings into the page — the author list, year and DOI are all still pending, and
a hand-written string will not update when they land.

**What to cite.** Three things, and the relationship between them:

1. the dataset, by DOI, with the version;
2. the dataset paper, once published;
3. the portal landing page as the canonical location.

State that the dataset and the paper are cited together, not interchangeably.

**Version discipline.** Publications must state the version used. Each major
version gets its own DOI; minor updates share it with version notes. Old versions
are never overwritten. Link to `/datasets/checkpd/versions/` (job 06).

**Acknowledgement.** The wording the DUA requires — the Parkinson's Disease Center
of Excellence and the Thai Red Cross Society. If exact wording is not settled,
mark it pending rather than drafting it.

**Authors.** `dataset.authors` is `["TODO - author list pending"]`. Render a
visible pending state; do not omit the field and do not guess names.

## Acceptance

Beyond the shared checklist in [00-README.md](00-README.md):

- [ ] Every citation string comes from `citations()`, none hand-written.
- [ ] The Zenodo record is unambiguously described as documentation only.
- [ ] The reason both DOIs resolve to one URL is stated.
- [ ] All three formats have working copy buttons.
- [ ] Pending DOI and pending authors render visibly, not as blanks.
- [ ] Version-in-publication requirement is stated.
