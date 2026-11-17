"""Build a PROVISIONAL cohort summary from a pre-release acquisition manifest.

`build_summary.py` summarises a finished release: every availability flag there
was verified against a file on disk. This script summarises a cohort that has
been selected but whose signal files have not been downloaded yet, so its
availability figures come from the acquisition manifest instead — what the
backend says was recorded, not what has been checked.

That distinction is the whole reason this is a separate script with a separate
output file. `CheckPD_Local_Agent_Context.md` Sec. 5 is explicit:

    Availability flags must be derived from files actually present on disk, not
    from intended collection flags.

Manifest-derived numbers do not meet that bar. They are useful for planning and
for showing cohort composition early, and they are published only when labelled
provisional. Every figure this script emits carries `provenance:
"acquisition_manifest"` and the payload carries `provisional: true`, so a page
cannot render them as verified by accident.

The manifest also contains `thaiid`, `user_id` and absolute timestamps - more
sensitive than the release tree this project's other summary reads. The same
identifier guard runs before anything is written.

Usage:
    python scripts/build_cohort_summary.py --manifest <record_id_filtered_*.csv> \\
                                           --version 2.1 --out src/data/summary-v2.1.json
"""

from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path

DIAGNOSIS_LABELS = {"pd": "PD", "PD": "PD", "ctrl": "HC", "hc": "HC", "HC": "HC"}
GROUPS = ["PD", "HC"]

# (canonical flag, manifest columns that feed it, display label)
# A modality is available when ANY of its manifest columns is true, which is how
# the two-handed tasks and the two voice tasks roll up.
MODALITIES = [
    ("voice_available", ("has_voiceAhh", "has_voiceYPL"), "Voice (any)"),
    ("voiceAhh_available", ("has_voiceAhh",), "Voice — sustained /a/"),
    ("voiceYPL_available", ("has_voiceYPL",), "Voice — connected speech"),
    ("tremor_resting_available", ("has_tremorResting",), "Tremor — resting"),
    ("tremor_postural_available", ("has_tremorPostural",), "Tremor — postural"),
    ("balance_available", ("has_balance",), "Balance"),
    ("gaitwalk_available", ("has_gaitWalk",), "Gait"),
    ("questionnaire_available", ("has_questionnaire",), "Questionnaire (20 items)"),
    ("dual_tap_available", ("has_dualTap", "has_dualTapRight"), "Dual-tap"),
    ("pinch_to_size_available", ("has_pinchToSize", "has_pinchToSizeRight"), "Pinch-to-size"),
]

PLAUSIBLE_AGE = (18, 110)
AGE_BIN_WIDTH = 10

FORBIDDEN_KEY = re.compile(
    r"thaiid|subject_id|patient_id|user_id|record_id|national_id|hospital_id"
    r"|prefix|phone|email|address|device_serial|timestamp",
    re.IGNORECASE,
)
FORBIDDEN_VALUE = re.compile(
    r"\b\d{13}\b"
    r"|\bS\d{4}\b"
    r"|[\w.+-]+@[\w-]+\.[\w.]+"
    r"|\b0\d{8,9}\b"
)


def truthy(value: str) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "y"}


def describe(values: list[int]) -> dict | None:
    if not values:
        return None
    ordered = sorted(values)
    mid = len(ordered) // 2
    median = ordered[mid] if len(ordered) % 2 else (ordered[mid - 1] + ordered[mid]) / 2
    return {
        "n": len(ordered),
        "min": ordered[0],
        "max": ordered[-1],
        "median": median,
        "mean": round(sum(ordered) / len(ordered), 1),
    }


def count_by(rows, key):
    counts = collections.Counter(r[key] for r in rows if (r.get(key) or "").strip())
    return [{"label": k, "count": v} for k, v in counts.most_common()]


def retention_reference(ref_manifest: Path, ref_summary: Path) -> dict | None:
    """Measure how far a previous release's manifest figures moved once its files
    were verified, per modality.

    "Provisional" on its own tells a reader nothing about magnitude. CheckPD v2.0
    kept 97.5-100% of its manifest counts for the inertial, questionnaire and
    touchscreen tasks, but only 63% for voiceAhh - voice passes through a separate
    segmentation pipeline that discards clips, while the others are cleaned in
    place. A reader needs that number to know which figures are nearly final and
    which will move by a third.
    """
    if not (ref_manifest.exists() and ref_summary.exists()):
        return None

    verified = {
        m["flag"]: m["total"]
        for m in json.loads(ref_summary.read_text(encoding="utf-8"))["modalities"]
    }
    claimed = {m["flag"]: m["total"] for m in summarise(ref_manifest, "reference")["modalities"]}

    per_modality = {}
    for flag, claim in claimed.items():
        if flag in verified and claim:
            per_modality[flag] = round(verified[flag] / claim, 4)

    return {
        "source_version": "2.0",
        "manifest": ref_manifest.name,
        "note": (
            "Fraction of each modality's manifest count that survived into the "
            "released files of CheckPD v2.0. Voice is preprocessed through a "
            "separate segmentation pipeline that discards clips; the other "
            "modalities are cleaned in place."
        ),
        "kept_fraction": per_modality,
    }


def summarise(manifest: Path, version: str) -> dict:
    with manifest.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fields = list(reader.fieldnames or [])
        rows = [dict(r) for r in reader]

    dx_col = "diagnosis" if "diagnosis" in fields else "condition"
    for row in rows:
        raw = (row.get(dx_col) or "").strip()
        row["_dx"] = DIAGNOSIS_LABELS.get(raw, raw.upper() or "UNKNOWN")

    by_group = {g: [r for r in rows if r["_dx"] == g] for g in GROUPS}
    unexpected = sorted({r["_dx"] for r in rows} - set(GROUPS))

    modalities = []
    for canonical, sources, label in MODALITIES:
        present = [c for c in sources if c in fields]
        if not present:
            continue
        counts = {
            g: sum(1 for r in by_group[g] if any(truthy(r.get(c, "")) for c in present))
            for g in GROUPS
        }
        modalities.append({
            "flag": canonical,
            "label": label,
            "source_column": ", ".join(present),
            "derived": None,
            "total": sum(counts.values()),
            "by_group": [{"label": g, "count": counts[g]} for g in GROUPS],
            # Nothing has been downloaded, so there is nothing to count. Emitting
            # 0 would read as "no files exist"; null reads as "not yet known".
            "files_on_disk": None,
        })

    lo, hi = PLAUSIBLE_AGE
    missing = implausible = 0
    ages = {g: [] for g in GROUPS}
    for row in rows:
        raw = (row.get("age") or "").strip()
        if not raw.replace(".", "", 1).lstrip("-").isdigit():
            missing += 1
            continue
        value = int(float(raw))
        if not (lo <= value <= hi):
            implausible += 1
            continue
        if row["_dx"] in ages:
            ages[row["_dx"]].append(value)

    usable = [a for values in ages.values() for a in values]
    bins = []
    if usable:
        start = (min(usable) // AGE_BIN_WIDTH) * AGE_BIN_WIDTH
        end = (max(usable) // AGE_BIN_WIDTH) * AGE_BIN_WIDTH
        for edge in range(start, end + AGE_BIN_WIDTH, AGE_BIN_WIDTH):
            bins.append({
                "label": f"{edge}–{edge + AGE_BIN_WIDTH - 1}",
                "by_group": [
                    {"label": g,
                     "count": sum(1 for a in ages[g] if edge <= a < edge + AGE_BIN_WIDTH)}
                    for g in GROUPS
                ],
            })

    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "version": version,
        "provisional": True,
        "provenance": "acquisition_manifest",
        "provenance_note": (
            "Availability is what the acquisition backend recorded, not a count of "
            "released files. Nothing here has been verified against a file on disk. "
            "These figures are superseded once the release tree is built."
        ),
        "source": manifest.name,
        "cohort": {
            "total": len(rows),
            "groups": [{"label": g, "count": len(by_group[g])} for g in GROUPS],
            "unexpected_labels": unexpected,
        },
        "modalities": modalities,
        "age": {
            "plausible_range": list(PLAUSIBLE_AGE),
            "bin_width": AGE_BIN_WIDTH,
            "reported": len(usable),
            "missing": missing,
            "excluded_implausible": implausible,
            "bins": bins,
            "overall": describe(usable),
            "by_group": {g: describe(ages[g]) for g in GROUPS},
        },
        "demographics": {
            "sex": count_by(rows, "gender"),
            "area": count_by(rows, "area"),
            "education_status": count_by(rows, "educationstatus"),
            "province_count": len({
                r["province_en"] for r in rows if (r.get("province_en") or "").strip()
            }),
        },
        "release": {"total_files": None, "total_bytes": None},
    }


def assert_no_identifiers(payload: dict) -> None:
    problems: list[str] = []

    def walk(node, path="$"):
        if isinstance(node, dict):
            for key, value in node.items():
                if FORBIDDEN_KEY.search(str(key)):
                    problems.append(f"{path}.{key}: forbidden key")
                walk(value, f"{path}.{key}")
        elif isinstance(node, list):
            for item in node:
                walk(item, f"{path}[]")
        elif isinstance(node, str) and FORBIDDEN_VALUE.search(node):
            problems.append(f"{path}: forbidden value {node!r}")

    walk(json.loads(json.dumps(payload)))
    if problems:
        raise SystemExit(
            "PII guard failed — refusing to write the cohort summary:\n  "
            + "\n  ".join(problems)
        )


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--version", default="2.1")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--reference-manifest", type=Path, default=None,
                        help="A previous release's manifest, to measure how far "
                             "manifest figures moved once its files were verified")
    parser.add_argument("--reference-summary", type=Path,
                        default=here.parent / "src" / "data" / "summary-v2.0.json")
    args = parser.parse_args()

    out = args.out or here.parent / "src" / "data" / f"summary-v{args.version}.json"
    if not args.manifest.exists():
        sys.exit(f"manifest not found: {args.manifest}")

    payload = summarise(args.manifest.resolve(), args.version)

    if args.reference_manifest:
        reference = retention_reference(args.reference_manifest.resolve(),
                                        args.reference_summary.resolve())
        if reference:
            payload["retention_reference"] = reference
            kept = reference["kept_fraction"]
            for modality in payload["modalities"]:
                fraction = kept.get(modality["flag"])
                modality["expected_after_verification"] = (
                    round(modality["total"] * fraction) if fraction else None
                )
                modality["kept_fraction_v2_0"] = fraction

    assert_no_identifiers(payload)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    groups = ", ".join(f"{g['label']}={g['count']}" for g in payload["cohort"]["groups"])
    print(f"wrote {out}")
    print(f"  version     {payload['version']}  (PROVISIONAL - {payload['provenance']})")
    print(f"  manifest    {args.manifest.name}")
    print(f"  cohort      {payload['cohort']['total']}  ({groups})")
    print(f"  age         {payload['age']['reported']} reported, "
          f"{payload['age']['missing']} missing, "
          f"{payload['age']['excluded_implausible']} implausible")
    print(f"  modalities  {len(payload['modalities'])} (files_on_disk: not yet known)")
    if payload.get("retention_reference"):
        print("  projected after file verification, using v2.0 retention:")
        for modality in payload["modalities"]:
            fraction = modality.get("kept_fraction_v2_0")
            if fraction is None:
                continue
            marker = "  <-- moves a lot" if fraction < 0.8 else ""
            print(f"    {modality['flag']:<28} {modality['total']:>5} -> "
                  f"~{modality['expected_after_verification']:<6} "
                  f"({fraction:.0%} kept in v2.0){marker}")
    if payload["cohort"]["unexpected_labels"]:
        print(f"  !! unexpected diagnosis labels: {payload['cohort']['unexpected_labels']}")


if __name__ == "__main__":
    main()
