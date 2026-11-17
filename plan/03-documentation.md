# Job 03 — Documentation index and modality pages

**Task:** PLAN.md B7
**Routes:** `/datasets/checkpd/v2.0/documentation/` and eight modality pages
**Files:** `src/pages/datasets/checkpd/v2.0/documentation/index.astro` plus
`src/content/modalities/*.md` rendered through a dynamic route

Read [00-README.md](00-README.md) first. This is the largest job; it can be split
between the index and the modality pages.

---

## Goal

Everything a researcher needs to interpret the files correctly. Documentation risk
is a named project risk: if people cannot read the data, the release fails
regardless of how good it is.

## Structure

Use an Astro content collection so the eight modality documents are Markdown, not
`.astro`. Clinicians should be able to edit them without touching components.

```
src/content/modalities/voice.md
                      /tremor-resting.md
                      /tremor-postural.md
                      /balance.md
                      /gaitwalk.md
                      /dual-tap.md
                      /pinch-to-size.md
                      /questionnaire.md
src/content.config.ts                        collection schema
src/pages/datasets/checkpd/v2.0/documentation/index.astro
src/pages/datasets/checkpd/v2.0/documentation/[slug].astro
```

Slugs must match `dataset.modalityDocs[].slug` exactly — that array already
carries the slug, label and a one-line blurb.

Frontmatter schema: `title`, `slug`, `summary`, `flag` (the `summary.json`
availability flag, so the page can show its own coverage), `status`
(`"complete" | "partial"`).

## Index page

Cohort-level orientation, then a card grid of the eight modality pages using
`dataset.modalityDocs`. Each card shows the label, the blurb, and the participant
count pulled from `summary.modalities` by matching `flag` — do not type counts
into the Markdown.

Also link, with pending labels where they do not exist yet: `data_dictionary.csv`
(task A4), `file_index.csv` (task A5), the technical validation report, and the
preprocessing protocol.

## Modality pages

Each covers, per `CheckPD_Local_Agent_Context.md` §5.2:

task protocol · sensor used · file format · sampling rate · units ·
preprocessing steps · quality control rules · example file structure

Source material — use it, do not invent beyond it:

**Voice** (§8). WAV, mono, 16 kHz, ~5 s. `voiceAhh` is sustained phonation,
manually segmented to a stable phonatory segment. `voiceYPL` is connected speech
processed with voice activity detection to remove silent intervals. QC: readable,
mono, 16 kHz, duration 4.5–5.5 s.

**Inertial** — tremor resting, tremor postural, balance, gaitwalk (§9). Shared
JSON schema with `subject_id`, `modality`, `sampling_rate_hz`, `units`,
`channels`, `data[]`. Channels are exactly `gx, gy, gz, ax, ay, az`. Gyroscope
`rad/s`, accelerometer `m/s²`. `t` is relative seconds from 0 — no absolute
timestamps. Sampling rate is estimated per file and is approximately 40 Hz; files
outside 20–100 Hz were flagged and excluded, and non-increasing timestamps were
removed before estimating. Include the example JSON block from §9.

**Touchscreen** — dual-tap, pinch-to-size (§10). Fields: `subject_id`,
`modality`, `hand`, `screen_metadata_available`, `units`, `data`. One file per
hand. **§10 requires an explicit statement of what was standardised and what
remains device-dependent** — screen size, pixel density and calibration vary
across handsets. Say this plainly; it is a limitation reviewers will look for.

**Questionnaire** (§7). 20 binary items, `0 = No`, `1 = Yes`. Render the item
table from `questionnaire_schema.csv` — `question_id`, `question_text_en`,
`question_text_th`, `response_type`, `encoding`.

The schema is supposed to carry a `domain` column (motor, sleep, sensory_gi,
neuropsych_cognitive, autonomic, red_flag) and **does not yet** — task A6. Until
it does, render the 20 items ungrouped and state that domain grouping is pending
clinical review. Do not assign domains yourself.

## The hard constraint on this job

`CheckPD_Local_Agent_Context.md` §20 lists twelve open clinical questions,
including the exact task protocols for balance, gait, tremor, tap, pinch and
voice, the device models used, and the app version per release.

**Those protocol details are not known.** Render them as a visible `TODO — pending
clinical team` block on each page. Writing a plausible-sounding protocol is
forbidden (`AGENTS.md` §4 rule 5) and is the single worst failure mode for this
job: a fabricated protocol is worse than an absent one, because nobody can tell it
is wrong.

Set `status: "partial"` in frontmatter for any page carrying a TODO, and surface
that on the index so the gap is visible rather than buried.

## Acceptance

Beyond the shared checklist in [00-README.md](00-README.md):

- [ ] Eight pages exist, slugs match `dataset.modalityDocs`.
- [ ] Every coverage count comes from `summary.json` via `flag`, not from Markdown.
- [ ] No invented protocol detail. Every unknown is a visible TODO.
- [ ] The touchscreen pages state what is device-dependent.
- [ ] The questionnaire page renders all 20 items and explains why they are ungrouped.
- [ ] Inertial pages state units, channel order, relative time, and the 20–100 Hz rule.
- [ ] The index shows which pages are partial.
