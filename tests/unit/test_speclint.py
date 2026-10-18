"""Unit tests for speclint checks."""

import ast
import sys
import unittest
from pathlib import Path

from src.speclint import (
    check_baseline,
    check_justified,
    check_no_mandates,
    check_observable,
    check_unique_ids,
    extract_baseline,
    lint,
    parse_rule_rows,
)

FIX = Path(__file__).resolve().parents[2] / "fixtures"
SPEC_CANDIDATES = [
    Path("/home/thoth/chat/workflow-spec/spec.md"),
    Path(__file__).resolve().parents[2] / "spec.md",
]


def find_real_spec() -> Path | None:
    for p in SPEC_CANDIDATES:
        if p.exists():
            return p
    return None


class TestUniqueIds(unittest.TestCase):
    def test_good_has_no_duplicates(self):
        text = (FIX / "good.md").read_text()
        ok, _, _ = check_unique_ids(text)
        self.assertEqual(ok, True)

    def test_dup_fails(self):
        text = (FIX / "bad-dup.md").read_text()
        ok, msg, _ = check_unique_ids(text)
        self.assertEqual(ok, False)
        self.assertIn("B1", msg)

    def test_real_spec_39_unique(self):
        spec = find_real_spec()
        if spec is None:
            self.skipTest("real spec.md not present in this checkout")
        text = spec.read_text()
        ok, msg, ids = check_unique_ids(text)
        self.assertEqual(ok, True, msg)
        self.assertEqual(len(ids), 39)


class TestJustified(unittest.TestCase):
    def test_good_passes(self):
        rows = parse_rule_rows((FIX / "good.md").read_text())
        self.assertGreater(len(rows), 0)
        ok, _ = check_justified(rows)
        self.assertEqual(ok, True)

    def test_missing_failure_fails(self):
        rows = parse_rule_rows((FIX / "bad-justified.md").read_text())
        self.assertGreater(len(rows), 0)
        ok, msg = check_justified(rows)
        self.assertEqual(ok, False)
        self.assertIn("T1", msg)


class TestObservable(unittest.TestCase):
    def test_good_passes(self):
        rows = parse_rule_rows((FIX / "good.md").read_text())
        ok, _ = check_observable(rows)
        self.assertEqual(ok, True)

    def test_easy_fails(self):
        rows = parse_rule_rows((FIX / "bad-observable.md").read_text())
        ok, msg = check_observable(rows)
        self.assertEqual(ok, False)
        self.assertIn("T1", msg)


class TestNoMandates(unittest.TestCase):
    def test_good_passes(self):
        ok, _ = check_no_mandates((FIX / "good.md").read_text())
        self.assertEqual(ok, True)

    def test_lane_mandate_fails(self):
        ok, _ = check_no_mandates((FIX / "bad-mandate.md").read_text())
        self.assertEqual(ok, False)

    def test_real_spec_passes(self):
        spec = find_real_spec()
        if spec is None:
            self.skipTest("real spec.md not present")
        ok, msg = check_no_mandates(spec.read_text())
        self.assertEqual(ok, True, msg)


class TestBaseline(unittest.TestCase):
    def test_good_is_one_page(self):
        ok, _, stats = check_baseline((FIX / "good.md").read_text())
        self.assertEqual(ok, True)
        self.assertLessEqual(stats["wrapped_lines"], 55)

    def test_overflow_fails(self):
        ok, _, _ = check_baseline((FIX / "bad-baseline.md").read_text())
        self.assertEqual(ok, False)

    def test_extract_present(self):
        base = extract_baseline((FIX / "good.md").read_text())
        self.assertIn("Principles", base)


class TestStdlibOnly(unittest.TestCase):
    def test_no_external_imports(self):
        src = Path(__file__).resolve().parents[2] / "src" / "speclint.py"
        tree = ast.parse(src.read_text())
        stdlib = set(sys.stdlib_module_names)
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    imported.add(a.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported.add(node.module.split(".")[0])
        external = {m for m in imported if m not in stdlib}
        self.assertEqual(external, set(), f"external imports: {external}")


class TestLintEndToEnd(unittest.TestCase):
    def test_good_passes_overall(self):
        result = lint(FIX / "good.md")
        self.assertEqual(result["pass"], True)

    def test_each_bad_fails(self):
        for name in [
            "bad-dup.md",
            "bad-justified.md",
            "bad-observable.md",
            "bad-mandate.md",
            "bad-baseline.md",
        ]:
            with self.subTest(fixture=name):
                result = lint(FIX / name)
                self.assertEqual(result["pass"], False, name)


if __name__ == "__main__":
    unittest.main()
