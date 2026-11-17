"""Compare the sitemap's route list against what the build actually emitted.

`src/data/routes.ts` is maintained by hand, so it can drift from the pages that
exist. This fails loudly instead, and also checks that the generated sitemap and
robots.txt point at the same host the build was configured for.

Run after a build:
    python scripts/check_routes.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / "dist"


def built_routes() -> set[str]:
    return {
        "/" if page.parent == DIST else f"/{page.parent.relative_to(DIST).as_posix()}/"
        for page in DIST.rglob("index.html")
    }


def main() -> int:
    if not DIST.is_dir():
        sys.exit("no dist/ - run a build first")

    sitemap = DIST / "sitemap-0.xml"
    if not sitemap.exists():
        sys.exit("no dist/sitemap-0.xml")

    locs = re.findall(r"<loc>([^<]+)</loc>", sitemap.read_text(encoding="utf-8"))
    hosts = {re.match(r"(https?://[^/]+)", loc).group(1) for loc in locs}
    listed = {re.sub(r"https?://[^/]+", "", loc) or "/" for loc in locs}
    built = built_routes()

    problems: list[str] = []

    missing = sorted(built - listed)
    extra = sorted(listed - built)
    if missing:
        problems.append(f"built but not in the sitemap: {', '.join(missing)}")
    if extra:
        problems.append(f"in the sitemap but not built: {', '.join(extra)}")
    if len(hosts) != 1:
        problems.append(f"sitemap mixes hosts: {', '.join(sorted(hosts))}")

    robots = DIST / "robots.txt"
    if not robots.exists():
        problems.append("robots.txt was not generated")
    else:
        text = robots.read_text(encoding="utf-8")
        blocked = "Disallow: /" in text
        noindexed = '<meta name="robots" content="noindex' in (
            DIST / "index.html"
        ).read_text(encoding="utf-8")
        if blocked != noindexed:
            problems.append(
                "robots.txt and the page meta disagree: "
                f"robots blocks={blocked}, pages noindex={noindexed}"
            )
        # A blocked build must not also be advertising a sitemap.
        if blocked and "Sitemap:" in text:
            problems.append("demo robots.txt still advertises a sitemap")

    host = next(iter(hosts)) if len(hosts) == 1 else "?"
    mode = "demo" if (DIST / "robots.txt").exists() and "Disallow: /" in (
        DIST / "robots.txt"
    ).read_text(encoding="utf-8") else "production"

    if problems:
        print(f"FAIL ({mode}, {host})")
        for problem in problems:
            print(f"  {problem}")
        return 1

    print(f"OK  {mode} build, host {host}, {len(built)} routes, sitemap in sync")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
