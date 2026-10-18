"""Integration: run CLI as subprocess on fixtures."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIX = ROOT / "fixtures"


def run_cli(spec: Path, fmt: str = "text") -> subprocess.CompletedProcess:
    cmd = [sys.executable, "-m", "src.speclint", str(spec)]
    if fmt == "json":
        cmd += ["--format", "json"]
    return subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=20)


class TestCliIntegration(unittest.TestCase):
    def test_good_text_passes(self):
        proc = run_cli(FIX / "good.md")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("TOTAL PASS", proc.stdout)

    def test_bad_each_fails(self):
        for name in [
            "bad-dup.md",
            "bad-justified.md",
            "bad-observable.md",
            "bad-mandate.md",
            "bad-baseline.md",
        ]:
            with self.subTest(fixture=name):
                proc = run_cli(FIX / name)
                self.assertNotEqual(proc.returncode, 0, name)
                self.assertIn("FAIL", proc.stdout, name)

    def test_good_json_shape(self):
        proc = run_cli(FIX / "good.md", fmt="json")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["pass"], True)
        self.assertEqual(len(payload["checks"]), 5)
        names = {c["name"] for c in payload["checks"]}
        self.assertEqual(
            names,
            {
                "unique_ids",
                "justified",
                "observable_triggers",
                "no_mandates",
                "baseline_size",
            },
        )


if __name__ == "__main__":
    unittest.main()
