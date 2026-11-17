# Job 04 — Access levels, DUA, and the request form

**Task:** PLAN.md B8
**Routes:** `/datasets/checkpd/v2.0/access/` and `/access/`
**Files:** `src/pages/datasets/checkpd/v2.0/access/index.astro`,
`src/pages/access/index.astro`

Read [00-README.md](00-README.md) first.

---

## Goal

Two pages with different jobs:

- `/access/` — portal-wide policy. The three access levels, the approval process,
  the DUA, and the governance position. Stable across future datasets.
- `/datasets/checkpd/v2.0/access/` — how to request *this* dataset. Short, linking
  to `/access/` for policy rather than repeating it.

## `/access/` — policy

**The three levels**, per `writing-block.md` §5.4:

| Level | Name | Unlocks |
|---|---|---|
| 1 | Public metadata | Description, cohort and modality summaries, documentation, data dictionary, citation. No registration. |
| 2 | Registered access | Example files, sample dataset, code examples. Basic registration. |
| 3 | Credentialed access | Full release: signal files, clinical scores, complete metadata table. Approved request + signed DUA. |

**Approval workflow**, stated plainly so applicants know what to expect: submit →
curator review → DUA signature → time-limited download link issued → access
logged. Do not state a turnaround time; C8 has not set one.

**Why credentialed rather than open.** The release carries health-related
questionnaire responses, clinical scores and sensor recordings. Also state what it
does *not* carry: no direct identifiers, no backend identifiers, no absolute
timestamps, no linkage table.

**DUA section** with `id="dua"` — the footer already links to `/access/#dua`.
Terms from `writing-block.md` §13: approved research purposes only; no
re-identification attempts; no redistribution; no combination with external data
for re-identification; report security incidents; cite the dataset and paper with
the correct version; acknowledge the Parkinson's Disease Center of Excellence and
the Thai Red Cross Society; follow applicable ethical and legal requirements.

**The DUA text is not final** (task C5), and the PDPA statement is not written
(task C3). Render both as clearly marked drafts or as `Pending` — never as text
someone could mistake for binding terms. This is the highest-risk page on the site
to get wrong.

## `/datasets/checkpd/v2.0/access/` — request

Access level from `dataset.accessLevel`. What approval unlocks, sized with figures
from `summary.json`. The request form. A link to `/access/` for full policy.

**Form fields** — per `writing-block.md` §5.4:

researcher name · institution · institutional email · research purpose ·
dataset version requested · agreement to the data use terms ·
confirmation of no re-identification attempt · agreement not to redistribute

**The form must not collect health data**, and must not ask for a national ID or
any patient information. It collects researcher identity and intent only.

**Where it posts is not decided** (PLAN Track C). Build the markup with a
`TODO: form endpoint` and no live `action`, or render a "request by email"
fallback using `portal.contactEmail`. Do not wire it to a third-party service on
your own initiative — that is a governance decision, and
`portal.contactEmail` is itself still a `TODO` placeholder.

Make every required field genuinely `required`, label every input (no
placeholder-as-label), and group the three agreements as real checkboxes with
visible text, not a single "I agree to the terms" line.

## Acceptance

Beyond the shared checklist in [00-README.md](00-README.md):

- [ ] No draft DUA text can be mistaken for final terms.
- [ ] PDPA statement shows as pending, not invented.
- [ ] Form collects no health data, no national ID, no patient information.
- [ ] Form is not wired to any external endpoint.
- [ ] Every input has a real `<label>`; agreements are separate checkboxes.
- [ ] `/access/#dua` resolves to the DUA section.
- [ ] The two pages do not duplicate each other.
- [ ] No turnaround time is promised.
