import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from app import run_analysis, run_score


class ProductTests(unittest.TestCase):
    def test_signal_relay_priority_is_traceable(self):
        result = run_score({"account": "Acme", "fit": 90, "intent": 80, "timing": 70, "confidence": 100})
        self.assertEqual(result["band"], "priority")
        self.assertTrue(result["approval_required"])
        self.assertEqual(result["mode"], "simulated")

    def test_signal_relay_rejects_bad_input(self):
        with self.assertRaises(Exception):
            run_score({"fit": 101, "intent": 10, "timing": 10, "confidence": 10})

    def test_deal_ledger_cites_and_leaves_gaps(self):
        result = run_analysis({"deal": "Acme", "transcript": "The economic buyer is Jo. Budget is not confirmed. Next step is to schedule a review."})
        statuses = {item["field"]: item["status"] for item in result["fields"]}
        self.assertEqual(statuses["economic_buyer"], "evidence_found")
        self.assertEqual(statuses["timeline"], "missing")
        self.assertEqual(result["write_status"], "proposed_only")


if __name__ == "__main__":
    unittest.main()
