"""Build current v2.1 summaries while preserving the separate v2.0 snapshot."""
import json
import subprocess
import sys
from pathlib import Path

from build_summary import assert_no_identifiers


def main():
    app = Path(__file__).resolve().parents[1]
    data = app / "src" / "data"
    frozen = data / "summary-v2.0.json"
    if not frozen.exists():
        raise SystemExit("Restore summary-v2.0.json or run npm run summary:v2.0 before building")
    assert_no_identifiers(json.loads(frozen.read_text(encoding="utf-8")))
    subprocess.run([sys.executable, str(app / "scripts/build_v21_summary.py")], check=True)
    payload = json.loads((data / "summary-v2.1-verified.json").read_text(encoding="utf-8"))
    if payload.get("version") != "2.1":
        raise SystemExit("Expected a validated v2.1 summary")
    assert_no_identifiers(payload)
    temp = data / "summary.json.tmp"
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    temp.replace(data / "summary.json")
    print("Current portal summary: v2.1; frozen v2.0 snapshot preserved")


if __name__ == "__main__":
    main()
