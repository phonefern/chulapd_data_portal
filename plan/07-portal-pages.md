# Job 07 — Publications, Documentation hub, About, Contact

**Task:** PLAN.md B11
**Routes:** `/publications/`, `/documentation/`, `/about/`, `/contact/`
**Files:** `src/pages/{publications,documentation,about,contact}/index.astro`

Read [00-README.md](00-README.md) first. Four small pages; the header nav already
links all of them, so they are currently broken links.

---

## `/publications/`

Links datasets to research outputs. Per `writing-block.md` §5.3, each entry
carries: title, authors, journal or conference, year, DOI, dataset version used,
and citation format.

**Almost nothing here is known yet.** The dataset paper is in preparation; the
platform paper, voice biomarker study and questionnaire model papers are not
confirmed in this repository.

Do not fabricate a publication list. Build the page as:

- A short explanation of what will be listed here.
- A "In preparation" entry for the CheckPD v2.0 dataset paper, with no journal,
  no year, no DOI — all `Pending`.
- A section for "Publications using this dataset", stating that external users
  are asked to notify the curator, and that entries will appear here.
- A pointer to `/datasets/checkpd/v2.0/citation/` for how to cite.

Structure the data as an array in the page (or a small content collection) so
adding a real publication later is a one-line change, not a rewrite.

A citation for a paper that does not exist yet is worse than an empty section.

## `/documentation/`

Portal-wide documentation hub, distinct from the dataset-specific documentation at
`/datasets/checkpd/v2.0/documentation/` (job 03). Keep it thin — it routes, it
does not duplicate.

- What documentation the portal provides for every release: README, data
  dictionary, file index, modality documentation, validation report, version history.
- A link through to the CheckPD v2.0 documentation.
- A short "how to work with a CheckPD release" orientation: `metadata.csv` is the
  index; join everything on `subject_id`; use `*_available` flags to build
  task-specific cohorts.

Include a worked code example, since `CheckPD_Local_Agent_Context.md` §3 supplies
one and users will copy it:

```python
import pandas as pd
meta = pd.read_csv("metadata.csv")

# Voice-only cohort
voice = meta.query("voiceAhh_available == 1 and voiceYPL_available == 1")

# Multimodal cohort
multi = meta.query(
    "voice_available == 1 and tremor_resting_available == 1 "
    "and questionnaire_available == 1"
)
```

These column names are correct as of the canonical schema — verify against
`summary.tables[0].column_names` before shipping, and if they disagree, the page
is wrong and must be fixed, not the check skipped.

## `/about/`

The portal, its operator, and its purpose. `portal.operator`, `portal.institution`.

- What the portal is: an institutional repository for clinician-confirmed digital
  biomarker datasets, not a general-purpose download host.
- Who runs it and under what institution.
- The commitments: versioned releases, frozen structures, documented access,
  long-term availability.
- Scope: Parkinson's disease and related neurological digital biomarker research,
  with room for future datasets.

Governance details — IRB number (`dataset.irb`), PDPA statement, license — are
`Pending`. Show them as pending; do not describe governance that is not settled.

## `/contact/`

Who to contact for what: dataset access requests, documentation questions,
reporting a data problem, publication notification.

`portal.contactEmail` is currently `TODO-portal-contact@chulapd.org` — a
placeholder, not a real address. **Do not print it as if it were live.** Render a
pending state, or route to the access request page. Publishing a fake address
would send real researchers' requests nowhere.

Name the institution and the centre; those are known.

## Acceptance

Beyond the shared checklist in [00-README.md](00-README.md):

- [ ] All four header nav links resolve.
- [ ] No fabricated publication, author, journal or DOI.
- [ ] The placeholder contact email is not presented as a working address.
- [ ] The code example's column names match `summary.tables[0].column_names`.
- [ ] `/documentation/` routes rather than duplicating job 03.
- [ ] Unsettled governance shows as pending.
