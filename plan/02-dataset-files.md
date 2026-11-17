# Job 02 — File structure and index

**Task:** PLAN.md B6
**Route:** `/datasets/checkpd/v2.0/files/`
**File:** `src/pages/datasets/checkpd/v2.0/files/index.astro`

Read [00-README.md](00-README.md) first.

---

## Goal

Tell a researcher exactly what they will receive before they request access, and
give them enough to write their loading code against. This page is the difference
between a usable dataset and one people give up on.

## Page content

**Breadcrumb** matching the landing page: Home / Datasets / CheckPD v2.0 / Files.

**Directory tree** in a `<pre>`. Mirror the structure documented in
`CheckPD_Local_Agent_Context.md` §4:

```
CheckPD_v2.0/
├── README.md
├── metadata.csv
├── clinical_scores.csv
├── questionnaire_responses.csv
├── questionnaire_schema.csv
├── data_dictionary.csv          (pending — task A4)
├── file_index.csv               (pending — task A5)
├── voice/
│   ├── voiceAhh/S####_voiceAhh.wav
│   └── voiceYPL/S####_voiceYPL.wav
├── tremor_resting/S####_tremor_resting.json
├── tremor_postural/S####_tremor_postural.json
├── balance/S####_balance.json
├── gaitwalk/S####_gaitwalk.json
├── dual_tap/S####_dual_tap_{left,right}.json
└── pinch_to_size/S####_pinch_{left,right}.json
```

Mark the two pending files as pending — they do not exist yet.

**Per-modality table** from `summary.modalities`: modality, participants with the
modality, `files_on_disk`. Explain the two rows where participants ≠ files:
`dual_tap` and `pinch_to_size` store one file per hand, so a participant
contributes one or two files. `voice_available` is a roll-up of `voiceAhh` and
`voiceYPL` and its `files_on_disk` is their sum — say so, or the totals look wrong.

Rows where `files_on_disk` is `null` are table-backed (questionnaire, clinical
scores); render an em dash and explain rather than showing `0`.

**Released tables** from `summary.tables`: file, rows, columns, size. For
`metadata.csv`, list its 30 column names from `column_names`, grouped the way
`DATA_RELEASE/README.md` groups them (identity / demographics / encoded /
availability flags). This is what people actually come here for.

**Naming convention.** `S####` subject IDs, zero-padded, contiguous from `S0001`.
State that no backend, hospital or patient identifier appears in any file, and
that timestamps inside signal files are relative seconds from zero.

**Integrity.** Once `file_index.csv` exists (task A5) it carries `sha256` per
file and is the way to verify a download. Say that it is coming; do not describe
it as available.

**Total size** from `summary.release` — files and bytes, formatted as GB.

## Constraints specific to this job

- **Never list individual filenames.** They contain subject IDs. Patterns only.
- Do not state a per-modality byte size unless you add it to
  `build_summary.py` first — it is not in `summary.json` today.

## Acceptance

Beyond the shared checklist in [00-README.md](00-README.md):

- [ ] No literal `S0001`-style ID anywhere in the output; `S####` patterns only.
- [ ] The participants-vs-files discrepancy is explained, not just displayed.
- [ ] `null` `files_on_disk` renders as an em dash with an explanation.
- [ ] All 30 `metadata.csv` columns are listed, grouped.
- [ ] Pending files are labelled pending.
