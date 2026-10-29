"""
Unit Tests for Handcrafted Cases (Case 01 and Case 02).
Verifies:
- All clue texts are max 20 words.
- All clues have image, lead reference, and allowed suspects.
- Exactly one culprit, one accomplice, and one forged clue per case.
- Mathematical solvability: true clues intersect to culprit, false clue triggers contradiction.
"""

import unittest
from game.cases import CASE_01, CASE_02

class TestCases(unittest.TestCase):
    def _test_case_integrity(self, case):
        culprit_id = case["culprit_id"]
        accomplice_id = case["accomplice_id"]
        forged_id = case["forged_clue_id"]
        suspect_ids = {s["id"] for s in case["suspects"]}

        self.assertIn(culprit_id, suspect_ids)
        self.assertIn(accomplice_id, suspect_ids)
        self.assertNotEqual(culprit_id, accomplice_id)

        # Clue text check (max 20 words)
        forged_count = 0
        true_sets = []
        forged_set = None

        for c in case["clues"]:
            word_count = len(c["desc"].split())
            self.assertLessEqual(word_count, 20, f"Clue {c['id']} exceeds 20 words: '{c['desc']}'")
            self.assertIn("image", c)
            self.assertIn("allowed", c)
            self.assertIn("lead_id", c)

            if c["is_forged"]:
                forged_count += 1
                self.assertEqual(c["id"], forged_id)
                forged_set = set(c["allowed"])
            else:
                true_sets.append(set(c["allowed"]))

        self.assertEqual(forged_count, 1, "Must have exactly one forged clue")

        # Solvability verification: intersection of true clues == {culprit_id}
        viable_true = set(suspect_ids)
        for s in true_sets:
            viable_true = viable_true.intersection(s)

        self.assertEqual(viable_true, {culprit_id}, f"True clues must narrow to culprit {culprit_id}")

        # Adding forged set causes empty set contradiction
        if forged_set:
            viable_contradiction = viable_true.intersection(forged_set)
            self.assertEqual(len(viable_contradiction), 0, "Forged clue must contradict true clues")

    def test_case_01(self):
        self._test_case_integrity(CASE_01)

    def test_case_02(self):
        self._test_case_integrity(CASE_02)

if __name__ == "__main__":
    unittest.main()
