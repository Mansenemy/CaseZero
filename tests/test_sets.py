"""
Unit Tests for SuspectSetEngine.
Verifies:
- Universe initialization
- Manual and evidence-based elimination (Universe \\ Eliminated)
- Mathematical set intersection across active clues
- Contradiction detection when intersection is the empty set (∅)
- Debunking false clues to restore viable candidates
"""

import unittest
from dsa.sets_engine import SuspectSetEngine

class TestSuspectSetEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SuspectSetEngine(["S1", "S2", "S3", "S4", "S5", "S6"])
        self.engine.register_clue("C1", ["S1", "S3", "S4", "S6"], "Left-Handed")
        self.engine.register_clue("C2", ["S1", "S2", "S4", "S5"], "Tier 3 Clearance")
        self.engine.register_clue("C3_LIE", ["S2", "S5"], "Petite Female", is_forged=True)

    def test_viable_without_forgery(self):
        res = self.engine.compute_viable(["C1", "C2"])
        # {S1, S3, S4, S6} ∩ {S1, S2, S4, S5} = {S1, S4}
        self.assertEqual(res["viable"], {"S1", "S4"})
        self.assertFalse(res["contradiction"])

    def test_contradiction_detection(self):
        # {S1, S4} ∩ {S2, S5} = ∅
        res = self.engine.compute_viable(["C1", "C2", "C3_LIE"])
        self.assertTrue(res["contradiction"])
        self.assertEqual(len(res["viable"]), 0)
        self.assertIn("C3_LIE", res["conflicting_clues"])

    def test_debunk_restores_viability(self):
        self.engine.debunk("C3_LIE")
        res = self.engine.compute_viable(["C1", "C2", "C3_LIE"])
        self.assertFalse(res["contradiction"])
        self.assertEqual(res["viable"], {"S1", "S4"})

    def test_elimination_and_restore(self):
        self.engine.eliminate("S1")
        res = self.engine.compute_viable(["C1", "C2"])
        self.assertEqual(res["viable"], {"S4"})

        self.engine.restore("S1")
        res2 = self.engine.compute_viable(["C1", "C2"])
        self.assertEqual(res2["viable"], {"S1", "S4"})

if __name__ == "__main__":
    unittest.main()
