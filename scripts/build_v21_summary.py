"""Refresh v2.1 portal aggregates only from a successfully validated run.

Does not modify the frozen v2.0 summary or read PRIVATE/id_map.csv. Backend IDs
in processing logs are never selected for output; only aggregate counts are used.
"""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from build_summary import summarise, assert_no_identifiers
from build_cohort_summary import summarise as summarise_manifest


def read_rows(path):
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def latest(directory, pattern):
    candidates = list(directory.glob(pattern))
    if not candidates:
        raise SystemExit(f"Missing required run artifact: {pattern}")
    return max(candidates, key=lambda p: (p.stat().st_mtime, p.name))


def main():
    app = Path(__file__).resolve().parents[1]
    runs = app.parents[1] / "CheckPD_v2.1" / "runs"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path)
    parser.add_argument("--out", type=Path, default=app / "src" / "data" / "summary-v2.1-verified.json")
    args = parser.parse_args()
    if args.run:
        run = args.run.resolve()
    else:
        pointer = json.loads((runs / "latest.json").read_text(encoding="utf-8"))
        run = runs / pointer["run_id"]
    state = json.loads((run / "run_manifest.json").read_text(encoding="utf-8"))
    if state.get("overall_status") != "ok" or not any(
        s["name"] == "migrate_07_validate" and s["status"] == "completed" for s in state["steps"]
    ):
        raise SystemExit("Refusing to publish aggregates from an unvalidated run")
    report = read_rows(latest(run / "csv", "validation_report_*.csv"))
    if any(row["severity"] == "error" for row in report):
        raise SystemExit("Release validation contains errors")
    release = run / "DATA_RELEASE"
    meta = read_rows(release / "metadata.csv")
    if not meta or any(row["dataset_version"] != "2.1" for row in meta):
        raise SystemExit("Expected a nonempty v2.1 metadata table")
    metrics = {r["metric"]: int(r["count"]) for r in read_rows(latest(run / "csv", "normalize_summary_*.csv"))}
    voice = read_rows(latest(run / "csv", "voice_ingest_log_*.csv"))
    feature = read_rows(latest(run / "csv", "motor_feature_log_*.csv"))
    flags = [f"{m}_data_incomplete" for m in ("tremor_resting", "tremor_postural", "balance", "gaitwalk")]
    payload = summarise(release)
    payload["version"] = "2.1"
    payload["known_gaps"] = {
        "voice_preprocessing_complete": not any(r["status"] == "failed" for r in voice),
        "voice_status_counts": dict(Counter(r["status"] for r in voice)),
        "voice_padded_files": sum(r["status"] == "processed" and r.get("padded") in {"1", "1.0"} for r in voice),
        "condition_conflict_groups_held": metrics.get("conflict:condition", 0) - metrics.get("resolved:condition_groups", 0),
        "condition_conflict_groups_resolved": metrics.get("resolved:condition_groups", 0),
        "condition_conflict_source_rows_held": metrics.get("held:condition_conflict_rows", 0),
        "incomplete_inertial_participants": sum(any(r.get(f) == "1" for f in flags) for r in meta),
        "incomplete_inertial_files": sum(r.get(f) == "1" for r in meta for f in flags),
        "partial_feature_rows": sum(r["status"] == "extracted" and r["data_incomplete"].lower() == "true" for r in feature),
        "feature_status_counts": dict(Counter(r["status"] for r in feature)),
    }
    assert_no_identifiers(payload)
    manifests = [p for p in (run / "csv").glob("record_id_filtered_*.csv")
                 if "voice_synced" not in p.stem]
    if not manifests:
        raise SystemExit("Missing original selected-cohort manifest")
    upstream = summarise_manifest(max(manifests, key=lambda p: (p.stat().st_mtime, p.name)), "2.1")
    assert_no_identifiers(upstream)
    output = args.out
    output.parent.mkdir(parents=True, exist_ok=True)
    (output.parent / "summary-v2.1.json").write_text(
        json.dumps(upstream, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"v2.1 summary: {payload['cohort']['total']} participants; privacy guard passed")
    print(f"Output: {output}")


if __name__ == "__main__":
    main()
