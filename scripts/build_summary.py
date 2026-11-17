"""Generate the aggregate dataset summary consumed by the CheckPD Data Portal.

Reads the frozen release tree and emits src/data/summary-v2.0.json.

Non-negotiable rules enforced here (CheckPD_Local_Agent_Context.md Sec. 23):
  * Rule 9   - every number the portal displays is derived from the release
               files themselves. Nothing in the web app is hand-typed.
  * Rule 1/2 - no subject-level row and no identifier of any kind may reach the
               generated file. Asserted before writing; the build fails loudly.

Usage:
    python scripts/build_summary.py [--release DIR] [--out FILE]
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

# --- Canonical schema ------------------------------------------------------
# The frozen release is expected to use the column names documented in
# CheckPD_Local_Agent_Context.md Sec. 5. The current v2.0 build still carries the
# older short names, so either is accepted and normalised to canonical. Once the
# release is renamed the aliases become dead entries and can be dropped.

DIAGNOSIS_COLUMNS = ("diagnosis", "condition")

DIAGNOSIS_LABELS = {"pd": "PD", "PD": "PD", "ctrl": "HC", "hc": "HC", "HC": "HC"}

GROUPS = ["PD", "HC"]

# (canonical flag, aliases, display label, release subdirectory)
MODALITIES = [
    ("voice_available", (), "Voice (any)", "voice"),
    ("voiceAhh_available", ("voice_ahh_available",), "Voice — sustained /a/", "voice/voiceAhh"),
    ("voiceYPL_available", ("voice_ypl_available",), "Voice — connected speech", "voice/voiceYPL"),
    ("tremor_resting_available", ("tremor_rest_available",), "Tremor — resting", "tremor_resting"),
    ("tremor_postural_available", ("tremor_post_available",), "Tremor — postural", "tremor_postural"),
    ("balance_available", (), "Balance", "balance"),
    ("gaitwalk_available", ("gait_available",), "Gait", "gaitwalk"),
    ("questionnaire_available", (), "Questionnaire (20 items)", None),
    # Dual-tap and pinch-to-size are withdrawn from the public dataset: circle-size
    # calibration is not comparable across handsets, so the recorded geometry
    # cannot be interpreted between participants.
    ("clinical_scores_available", (), "Clinical scores", None),
]

# Age values outside this range are treated as data-entry errors and excluded
# from the published distribution. They are reported, never silently dropped.
PLAUSIBLE_AGE = (18, 110)
AGE_BIN_WIDTH = 10

# Nothing matching these may appear in the generated summary.
FORBIDDEN_KEY = re.compile(
    r"subject_id|patient_id|user_id|record_id|national_id|hospital_id"
    r"|prefix|phone|email|address|device_serial",
    re.IGNORECASE,
)
FORBIDDEN_VALUE = re.compile(
    r"\b\d{13}\b"                   # Thai national ID
    r"|\bS\d{4}\b"                  # release subject ID
    r"|[\w.+-]+@[\w-]+\.[\w.]+"     # email address
    r"|\b0\d{8,9}\b"                # Thai phone number
)


def resolve(fieldnames, canonical, aliases=()):
    for candidate in (canonical, *aliases):
        if candidate in fieldnames:
            return candidate
    return None


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        return rows, list(reader.fieldnames or [])


def read_markdown_bullets(path: Path, heading: str) -> list[str]:
    """Read one generated README section without copying unrelated prose."""
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    in_section = False
    bullets = []
    for line in lines:
        if line.strip() == heading:
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.startswith("- "):
            bullets.append(line[2:].strip())
    return bullets


def count_by(rows, key):
    counts = collections.Counter(r[key] for r in rows if (r.get(key) or "").strip())
    return [{"label": k, "count": v} for k, v in counts.most_common()]


def describe(values):
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


def summarise(release: Path) -> dict:
    meta_rows, meta_fields = read_csv(release / "metadata.csv")

    dx_col = resolve(meta_fields, DIAGNOSIS_COLUMNS[0], DIAGNOSIS_COLUMNS[1:])
    if dx_col is None:
        sys.exit("metadata.csv has no diagnosis/condition column")

    for row in meta_rows:
        raw = (row.get(dx_col) or "").strip()
        row["_dx"] = DIAGNOSIS_LABELS.get(raw, raw.upper() or "UNKNOWN")

    by_group = {g: [r for r in meta_rows if r["_dx"] == g] for g in GROUPS}
    unexpected = sorted({r["_dx"] for r in meta_rows} - set(GROUPS))

    cohort = {
        "total": len(meta_rows),
        "groups": [{"label": g, "count": len(by_group[g])} for g in GROUPS],
        "unexpected_labels": unexpected,
    }

    # --- clinical scores ---------------------------------------------------
    clinical_path = release / "clinical_scores.csv"
    clinical_ids: set = set()
    clinical_fields: list = []
    if clinical_path.exists():
        clinical_rows, clinical_fields = read_csv(clinical_path)
        score_cols = [c for c in clinical_fields if c != "subject_id"]
        clinical_ids = {
            r["subject_id"] for r in clinical_rows
            if any((r.get(c) or "").strip() for c in score_cols)
        }

    # --- modality availability --------------------------------------------
    modalities = []
    for canonical, aliases, label, subdir in MODALITIES:
        col = resolve(meta_fields, canonical, aliases)
        derived = None
        if col is not None:
            counts = {g: sum(1 for r in by_group[g] if r.get(col) == "1") for g in GROUPS}
        elif canonical == "clinical_scores_available" and clinical_ids:
            counts = {
                g: sum(1 for r in by_group[g] if r["subject_id"] in clinical_ids)
                for g in GROUPS
            }
            derived = "derived from clinical_scores.csv (no flag column in metadata.csv)"
        else:
            continue

        files_on_disk = None
        if subdir:
            directory = release / subdir
            if directory.is_dir():
                files_on_disk = sum(1 for p in directory.rglob("*") if p.is_file())

        modalities.append({
            "flag": canonical,
            "label": label,
            "source_column": col,
            "derived": derived,
            "total": sum(counts.values()),
            "by_group": [{"label": g, "count": counts[g]} for g in GROUPS],
            "files_on_disk": files_on_disk,
        })

    # --- age ---------------------------------------------------------------
    lo, hi = PLAUSIBLE_AGE
    missing = implausible = 0
    ages = {g: [] for g in GROUPS}
    for row in meta_rows:
        raw = (row.get("age") or "").strip()
        try:
            # Accept "62" and "62.0" alike: a float-formatted age is untidy, not
            # missing, and treating it as missing silently zeroed the whole
            # column once.
            value = int(float(raw))
        except ValueError:
            missing += 1
            continue
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
                    {
                        "label": g,
                        "count": sum(1 for a in ages[g] if edge <= a < edge + AGE_BIN_WIDTH),
                    }
                    for g in GROUPS
                ],
            })

    age = {
        "plausible_range": list(PLAUSIBLE_AGE),
        "bin_width": AGE_BIN_WIDTH,
        "reported": len(usable),
        "missing": missing,
        "excluded_implausible": implausible,
        "bins": bins,
        "overall": describe(usable),
        "by_group": {g: describe(ages[g]) for g in GROUPS},
    }

    demographics = {
        "sex": count_by(meta_rows, "sex"),
        "area": count_by(meta_rows, "area"),
        "education_status": count_by(meta_rows, "education_status"),
        "income_band": count_by(meta_rows, "income_band"),
        "province_count": len({
            r["province"] for r in meta_rows if (r.get("province") or "").strip()
        }),
    }

    # --- release tables and size ------------------------------------------
    tables = []
    for name in ("metadata.csv", "clinical_scores.csv",
                 "questionnaire_responses.csv", "questionnaire_schema.csv"):
        path = release / name
        if not path.exists():
            continue
        rows, fields = read_csv(path)
        tables.append({
            "file": name,
            "rows": len(rows),
            "columns": len(fields),
            "column_names": fields,
            "bytes": path.stat().st_size,
        })

    # Questionnaire copy is release data, not editorial page content. Keeping
    # it in the generated payload means the documentation always reflects the
    # shipped schema without copying rows into an Astro or Markdown file.
    questionnaire_schema = []
    questionnaire_path = release / "questionnaire_schema.csv"
    if questionnaire_path.exists():
        questionnaire_rows, questionnaire_fields = read_csv(questionnaire_path)
        public_fields = [
            field for field in questionnaire_fields
            if field in {
                "question_id",
                "question_text_en",
                "question_text_th",
                "domain",
                "response_type",
                "encoding",
            }
        ]
        questionnaire_schema = [
            {field: row.get(field, "") for field in public_fields}
            for row in questionnaire_rows
        ]

    files = [p for p in release.rglob("*") if p.is_file()]
    release_changes = read_markdown_bullets(
        release / "README.md", "## Changes since v1.0"
    )
    if not release_changes:
        sys.exit("DATA_RELEASE/README.md has no Changes since v1.0 bullet list")

    # --- schema drift vs the documented canonical names --------------------
    drift = []
    if dx_col != "diagnosis":
        drift.append({"expected": "diagnosis", "found": dx_col})
    for canonical, aliases, _, _ in MODALITIES:
        found = resolve(meta_fields, canonical, aliases)
        if found is not None and found != canonical:
            drift.append({"expected": canonical, "found": found})
        elif found is None:
            drift.append({"expected": canonical, "found": None})

    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": str(release.name),
        "cohort": cohort,
        "modalities": modalities,
        "age": age,
        "demographics": demographics,
        "tables": tables,
        "questionnaire_schema": questionnaire_schema,
        "release": {
            "total_files": len(files),
            "total_bytes": sum(p.stat().st_size for p in files),
            "changes_since_v1": release_changes,
        },
        "clinical_score_columns": [c for c in clinical_fields if c != "subject_id"],
        "schema_drift": drift,
    }


def assert_no_identifiers(payload: dict) -> None:
    """Fail the build rather than publish anything subject-level."""
    problems = []

    # column_names legitimately contains the schema label "subject_id"; it is a
    # column name, not a value, so it is dropped before the scan.
    scrubbed = json.loads(json.dumps(payload))
    for table in scrubbed.get("tables", []):
        table.pop("column_names", None)

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

    walk(scrubbed)
    if problems:
        raise SystemExit(
            "PII guard failed — refusing to write summary.json:\n  " + "\n  ".join(problems)
        )


def main() -> None:
    here = Path(__file__).resolve().parent
    default_release = here.parent.parent.parent / "CheckPD_v2.0" / "DATA_RELEASE"

    parser = argparse.ArgumentParser()
    parser.add_argument("--release", type=Path, default=default_release)
    parser.add_argument("--out", type=Path, default=here.parent / "src" / "data" / "summary-v2.0.json")
    args = parser.parse_args()

    release = args.release.resolve()
    if not (release / "metadata.csv").exists():
        sys.exit(f"no metadata.csv under {release}")

    payload = summarise(release)
    assert_no_identifiers(payload)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    groups = ", ".join(f"{g['label']}={g['count']}" for g in payload["cohort"]["groups"])
    print(f"wrote {args.out}")
    print(f"  release     {release}")
    print(f"  subjects    {payload['cohort']['total']}  ({groups})")
    print(f"  modalities  {len(payload['modalities'])}")
    print(f"  files       {payload['release']['total_files']} "
          f"({payload['release']['total_bytes'] / 1e6:.0f} MB)")
    print(f"  age         {payload['age']['reported']} reported, "
          f"{payload['age']['missing']} missing, "
          f"{payload['age']['excluded_implausible']} implausible")
    if payload["schema_drift"]:
        print("  schema drift vs CheckPD_Local_Agent_Context.md Sec. 5:")
        for item in payload["schema_drift"]:
            print(f"    {item['expected']:<32} <- {item['found']}")


if __name__ == "__main__":
    main()
