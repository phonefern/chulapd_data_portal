# Job 08 — 404, sitemap, robots, and the final pass

**Task:** PLAN.md B12 and B15
**Files:** `src/pages/404.astro`, `public/robots.txt`, `astro.config.mjs`

Read [00-README.md](00-README.md) first. **Do this job last** — it links to and
checks whatever jobs 01–07 produced.

---

## 404 page

`src/pages/404.astro`. Static hosting serves it via nginx `error_page 404`.

Explain that the page does not exist, and offer routes out: the dataset landing
page, `/datasets/`, `/documentation/`, `/access/`.

**One thing matters more than the rest.** Someone hitting a 404 may have followed
a DOI or a citation in a published paper. Say explicitly that dataset URLs are
permanent and that if they arrived from a citation they should check the version
number, then link `/datasets/checkpd/versions/`. A generic "page not found" wastes
the one chance to recover a broken citation.

## Sitemap

`@astrojs/sitemap` is an official integration and `site` is already configured.

This adds a dependency, which needs an entry in
[`../../docs/DECISIONS.md`](../../docs/DECISIONS.md). If that is unwelcome, write
`public/sitemap.xml` by hand — there are around fifteen URLs and they change
rarely. Either is defensible; record which you chose and why.

## robots.txt

`public/robots.txt`. Allow crawling of the public portal — discoverability is the
point of the DOI landing page and its `schema.org/Dataset` markup.

```
User-agent: *
Allow: /
Sitemap: https://data.chulapd.org/sitemap-index.xml
```

Do not disallow anything here. The data files are not served from this origin;
they are gated by `secure_link` and are not linked from any page. Adding their
path to `robots.txt` would advertise it — a disallow line is a public statement
that something exists there.

## Final pass over every page (B15)

This is the part with real value. Jobs 01–07 each check themselves; this checks
the site as a whole.

**Links.** Every internal link resolves. No link to a page that was planned but
not built. Check the header and footer on every page, not just in `Header.astro`.

**Trailing slashes.** Config is `trailingSlash: 'always'`. Every internal href
must end in `/`, or nginx will redirect and the DOI target will take an extra hop.
Grep for `href="/[^"]*[^/"]"` and fix what it finds.

**Responsive.** Every page at 400 px with no horizontal scroll on `body`. The
22-bar availability chart and the wide tables are the likely failures.

**Themes.** White light mode is the default regardless of the operating-system
setting. Test every page in light and dark through the toggle, including the
saved preference restored before first paint. Look for any colour defined only
inside the explicit dark-theme block.

**Accessibility.** One `h1` per page; heading levels do not skip. Every form
control has a real label. Focus is visible on every interactive element. Tables
have `<th scope>`. The skip link works. Charts do not rely on colour alone.

**Consistency.** The same figure shows the same value everywhere — they all come
from `summary.json`, so a mismatch means someone typed a number. Find it.

**Pending states.** Every `Pending` is genuinely still pending. If a decision
landed while these pages were being built, update `dataset.ts`, not the page.

**Look at the pages.** Open them. A build log cannot show a label collision, an
overflowing table, or a chart squeezed to nothing. If you did not look, say so.

## Acceptance

- [ ] 404 page exists and addresses the broken-citation case.
- [ ] Sitemap generated or written; the choice recorded in `DECISIONS.md`.
- [ ] `robots.txt` allows crawling and does not name the data path.
- [ ] Every internal link resolves and ends in `/`.
- [ ] Every page passes at 400 px, in both themes.
- [ ] No figure disagrees with another page.
- [ ] `npm run build` clean; PII grep clean.
- [ ] `CHANGELOG.md` and `PLAN.md` updated.
