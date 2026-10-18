"""speclint: stdlib-only CLI that lints spec.md structural rules."""

import argparse
import json
import re
import sys
from pathlib import Path

ID_RE = re.compile(r"\b(B\d{1,2}|T\d|E\d|Y\d|CB\d)\b")
MANDATING_RE = re.compile(
    r"follow lane|tier gate|tier \d|freeze-required|freeze gate",
    re.IGNORECASE,
)
EASY_RE = re.compile(r"\b(easy|medium|hard)\b", re.IGNORECASE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_ids(text: str) -> list[str]:
    return ID_RE.findall(text)


RULE_ID_RE = re.compile(r"(?:\|\s*|\*\*)(B\d{1,2}|T\d|E\d|Y\d|CB\d)\b")


def check_unique_ids(text: str) -> tuple[bool, str, list[str]]:
    rows = parse_rule_rows(text)
    table_ids = [r["id"] for r in rows]
    bold_ids = RULE_ID_RE.findall(text)
    # Prefer structural IDs (tables + bold rule heads); fall back to raw
    # mentions only when no structural IDs exist.
    ids = bold_ids if bold_ids else table_ids
    if not ids:
        ids = extract_ids(text)
    seen: dict[str, int] = {}
    dups: list[str] = []
    for i in ids:
        seen[i] = seen.get(i, 0) + 1
        if seen[i] == 2:
            dups.append(i)
    unique_count = len(seen)
    if dups:
        return False, f"duplicate IDs: {', '.join(sorted(dups))}", sorted(seen.keys())
    return True, f"{unique_count} unique IDs, no duplicates", sorted(seen.keys())


def parse_rule_rows(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 5:
            continue
        first = cells[0]
        if not re.fullmatch(r"(B\d{1,2}|T\d|E\d|Y\d|CB\d)", first):
            continue
        if first == "ID":
            continue
        rows.append(
            {
                "id": first,
                "rule": cells[1] if len(cells) > 1 else "",
                "failure": cells[2] if len(cells) > 2 else "",
                "how": cells[3] if len(cells) > 3 else "",
                "applies": cells[4] if len(cells) > 4 else "",
            }
        )
    return rows


def check_justified(rows: list[dict[str, str]]) -> tuple[bool, str]:
    if not rows:
        return True, "no rule rows found, nothing to check"
    bad = [r["id"] for r in rows if not r["failure"] or not r["how"]]
    if bad:
        return False, f"rows missing Failure/How: {', '.join(sorted(bad))}"
    return True, f"{len(rows)} rows have Failure and How"


def check_observable(rows: list[dict[str, str]]) -> tuple[bool, str]:
    if not rows:
        return True, "no rule rows found, nothing to check"
    bad = [r["id"] for r in rows if EASY_RE.search(r["applies"])]
    if bad:
        return False, f"non-observable Applies (easy/medium/hard): {', '.join(sorted(bad))}"
    return True, f"{len(rows)} Applies cells observable"


def check_no_mandates(text: str) -> tuple[bool, str]:
    hits = MANDATING_RE.findall(text)
    if hits:
        return False, f"mandating lane/tier/freeze found: {', '.join(sorted(set(hits)))}"
    return True, "no mandating lane/tier/version-label/freeze"


def extract_baseline(text: str) -> str:
    start_markers = ["## 1. Principles", "# 1. Principles", "## 1."]
    end_markers = ["## 3. Triggered", "## 3.", "# 3."]
    start = -1
    for m in start_markers:
        idx = text.find(m)
        if idx != -1:
            start = idx
            break
    if start == -1:
        return ""
    end = len(text)
    for m in end_markers:
        idx = text.find(m, start + 1)
        if idx != -1:
            end = min(end, idx)
    return text[start:end]


def baseline_stats(baseline: str) -> dict[str, int]:
    lines = baseline.splitlines()
    chars = len(baseline)
    words = len(baseline.split())
    wrapped = 0
    for line in lines:
        wrapped += max(1, (len(line) + 89) // 90)
    return {
        "lines": len(lines),
        "words": words,
        "chars": chars,
        "wrapped_lines": wrapped,
    }


def check_baseline(text: str) -> tuple[bool, str, dict[str, int]]:
    base = extract_baseline(text)
    if not base:
        return False, "baseline section not found", {"lines": 0, "words": 0, "chars": 0, "wrapped_lines": 0}
    stats = baseline_stats(base)
    if stats["wrapped_lines"] <= 55:
        return True, (
            f"baseline {stats['lines']} lines, {stats['words']} words, "
            f"{stats['chars']} chars, wrapped {stats['wrapped_lines']} lines = 1 page"
        ), stats
    return False, (
        f"baseline too large: wrapped {stats['wrapped_lines']} lines > 55 "
        f"({stats['lines']} lines, {stats['words']} words)"
    ), stats


def lint(path: Path) -> dict:
    text = read_text(path)
    rows = parse_rule_rows(text)
    ok_ids, msg_ids, ids = check_unique_ids(text)
    ok_j, msg_j = check_justified(rows)
    ok_o, msg_o = check_observable(rows)
    ok_m, msg_m = check_no_mandates(text)
    ok_b, msg_b, stats = check_baseline(text)
    overall = ok_ids and ok_j and ok_o and ok_m and ok_b
    return {
        "file": str(path),
        "pass": overall,
        "checks": [
            {"name": "unique_ids", "pass": ok_ids, "detail": msg_ids},
            {"name": "justified", "pass": ok_j, "detail": msg_j},
            {"name": "observable_triggers", "pass": ok_o, "detail": msg_o},
            {"name": "no_mandates", "pass": ok_m, "detail": msg_m},
            {"name": "baseline_size", "pass": ok_b, "detail": msg_b, "stats": stats},
        ],
        "ids": ids,
        "rule_rows": len(rows),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint spec.md structural rules.")
    parser.add_argument("spec", help="Path to spec.md")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)
    result = lint(Path(args.spec))
    if args.format == "json":
        sys.stdout.write(json.dumps(result, indent=2) + "\n")
    else:
        for c in result["checks"]:
            mark = "PASS" if c["pass"] else "FAIL"
            sys.stdout.write(f"{mark} {c['name']}: {c['detail']}\n")
        sys.stdout.write(f"TOTAL {'PASS' if result['pass'] else 'FAIL'}\n")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
