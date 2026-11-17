# AGENTS.md — CheckPD Data Portal web app

Scoped rules for this directory. The repository-wide rules are in
[`../../AGENTS.md`](../../AGENTS.md); read that first.

Full specification: [`../docs/UI_SPEC.md`](../docs/UI_SPEC.md).
Task list: [`../docs/PLAN.md`](../docs/PLAN.md).

---

## Commands

```bash
npm install
npm run dev          # current v2.1 summaries, then astro dev on :4321
npm run build        # production build into dist/
npm run build:demo   # gated preview build - noindex, banner, preview-host URLs
npm run check:routes # sitemap vs built routes, and demo-mode consistency
npm run summary      # regenerate current v2.1 aggregates and summary.json
npm run brand        # regenerate public/brand/ from the logo sources
```

Run `check:routes` after any build that adds or removes a page. Build modes and
hosting are documented in [`../docs/DEPLOY.md`](../docs/DEPLOY.md).

`npm run dev` and `npm run build` both regenerate `summary.json` first. Running
`astro build` directly will silently use a stale summary — don't.

The default builder reads the validated v2.1 run selected by
`CheckPD_v2.1/runs/latest.json`. It preserves the restored, gitignored
`src/data/summary-v2.0.json` snapshot for the permanent v2.0 routes.
If that snapshot is missing, restore it or regenerate it with
`npm run summary:v2.0` (requires the frozen v2.0 release tree).
Use `python scripts/build_summary.py --release <dir>` for a different v2.0 path.

---

## The four rules that matter most here

**1. Never type a statistic into a page.**
Every count, percentage, size and date comes from `src/data/summary.json`, which
is generated from the release tree at build time. If the figure you need isn't
there, extend the appropriate summary builder. Version-specific pages use their
matching versioned summary; never attach current v2.1 counts to a v2.0 record. A hand-typed number is correct the day
it is typed and wrong forever after, and it puts the portal in silent
disagreement with the manuscript. (`CheckPD_Local_Agent_Context.md` §23 rule 9.)

**2. `src/data/dataset.ts` holds no counts.**
It is bibliographic and editorial only — title, version, DOI slots, author list,
citation builders. Counts live in `summary.json`. Keep the split clean.

**3. `/datasets/checkpd/v2.0/` is a DOI resolution target.**
It is frozen. Do not move it, rename it, or change the routing config that
produces it. Someone arriving there from a citation years from now, with no other
context, must find the dataset identified, described, and citable on that page.

**4. Unknown is `Pending`, visibly.**
License, DOI, IRB number, author list and DUA terms are not yet decided. They
render as a visible `Pending`. Never invent a plausible value and never quietly
omit the row — a missing row reads as "not applicable", which is a different and
wrong claim.

---

## Layout of this directory

```
scripts/build_summary.py     release tree → summary.json, with the PII guard
src/data/dataset.ts          bibliographic facts (hand-maintained, no counts)
src/data/summary.json        generated, gitignored — never edit, never commit
src/styles/tokens.css        all colour and layout tokens
src/layouts/Base.astro       document shell, theme bootstrap, copy handler
src/components/              Header, Footer, StatTiles, AvailabilityChart
src/pages/                   one directory per URL
```

---

## Conventions

**Colours.** Use tokens, never raw hex. Brand crimson is chrome only — header,
links, primary buttons — and never enters a plot area. Chart series are
`--series-pd` (blue) and `--series-hc` (orange), validated for colour-vision
deficiency in both themes. A third series takes the next slot from the validated
categorical order and is re-validated before shipping.

**Dark mode.** Define every colour on bare `:root` first, then redefine it in
*both* the `@media (prefers-color-scheme: dark)` block (guarded with
`:root:not([data-theme='light'])`) and the `:root[data-theme='dark']` block. A
colour whose only definition is inside one of those will break the other path.

**Dependencies.** One: `astro`. Do not add another without recording why in
[`../docs/DECISIONS.md`](../docs/DECISIONS.md). Charts are plain HTML and CSS on
purpose — no charting library. Sustainability is a named project risk.

**Responsive.** Every page must work at 400 px with no horizontal scroll on
`body`. Wide tables, code blocks and charts each get their own `.table-scroll`.

---

## The PII guard

`build_summary.py` runs `assert_no_identifiers()` before writing. Any
`subject_id`-shaped key, `S####` value, 13-digit number, email address or phone
number in the payload **aborts the build**.

If it fires, the answer is to stop aggregating subject-level data — not to relax
the guard. The release tree and `CheckPD_v2.0/PRIVATE/id_map.csv` live in the same
working tree, so a wrong `--release` argument is a realistic accident.

After building, confirm the output too:

```bash
grep -rlE '\bS[0-9]{4}\b|\b[0-9]{13}\b|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}' dist/
```

Expect no matches.

---

## Definition of done

The checklist is at the end of [`../docs/UI_SPEC.md`](../docs/UI_SPEC.md). At
minimum: `npm run build` passes, the `grep` above is clean, the page holds up at
400 px in both themes, and you have appended to
[`../docs/CHANGELOG.md`](../docs/CHANGELOG.md).

Visual layout is not verifiable from a build log. If you have not looked at the
page, say so rather than implying it was checked.
