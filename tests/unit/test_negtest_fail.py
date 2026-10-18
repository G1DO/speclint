"""Negtest CB1 fail - breaking one suite (delete after)."""
import unittest
class TestNegFail(unittest.TestCase):
    def test_break_gate(self):
        self.assertTrue(False, "negtest cb1-fail: intentional break")
