"""
Unit Tests for GameSession and End-to-End Playthrough.
Verifies complete investigation flow:
- Session initialization
- Lead exploration and AP deduction
- Forgery debunking and contradiction resolution
- BFS collusion path query
- Alibi binary search trace
- Accusation verdict and 1000+ scoring achievement
"""

import unittest
from game.state import GameSession

class TestGameSession(unittest.TestCase):
    def setUp(self):
        self.session = GameSession()
        self.session.start_case("case_1")

    def test_initial_state(self):
        state = self.session.to_dict()
        self.assertEqual(state["ap"], 12)
        self.assertEqual(len(state["suspects"]), 6)
        self.assertEqual(len(state["discovered_clues"]), 0)
        self.assertFalse(state["contradiction_detected"])

    def test_explore_leads_and_contradiction(self):
        # Explore L1 (costs 1 AP, reveals C1)
        r1 = self.session.explore_lead("L1")
        self.assertTrue(r1["success"])
        self.assertEqual(self.session.ap, 11)
        self.assertIn("C1", self.session.discovered_clues)

        # Explore L2 (costs 1 AP, reveals C2)
        r2 = self.session.explore_lead("L2")
        self.assertTrue(r2["success"])
        self.assertEqual(self.session.ap, 10)
        self.assertIn("C2", self.session.discovered_clues)

        # Explore L3 (costs 1 AP, reveals C3 - Forgery!)
        r3 = self.session.explore_lead("L3")
        self.assertTrue(r3["success"])
        self.assertEqual(self.session.ap, 9)
        self.assertIn("C3", self.session.discovered_clues)

        # State should now detect contradiction because (C1 ∩ C2) ∩ C3 = ∅
        state = self.session.to_dict()
        self.assertTrue(state["contradiction_detected"])
        self.assertEqual(len(state["viable_suspect_ids"]), 0)

        # Debunk C3
        debunk_res = self.session.debunk_clue("C3")
        self.assertTrue(debunk_res["success"])
        self.assertTrue(debunk_res["is_forged"])

        # Viable suspects should be restored to {S1, S4}
        state_restored = self.session.to_dict()
        self.assertFalse(state_restored["contradiction_detected"])
        self.assertEqual(set(state_restored["viable_suspect_ids"]), {"S1", "S4"})

    def test_alibi_check_binary_search(self):
        # Check S5 at 23:45 (Maya Lin's verified alibi)
        res = self.session.check_alibi("S5", "23:45")
        self.assertTrue(res["success"])
        self.assertTrue(res["alibi_holds"])
        self.assertFalse(res["alibi_broken"])
        self.assertEqual(self.session.ap, 11)  # Cost 1 AP

        # Check S4 at 23:45 (Viktor Drake's vault breach)
        res4 = self.session.check_alibi("S4", "23:45")
        self.assertTrue(res4["success"])
        self.assertTrue(res4["alibi_broken"])

    def test_query_path_bfs(self):
        # S4 to S6
        res = self.session.query_path("S4", "S6")
        self.assertTrue(res["success"])
        self.assertTrue(res["found"])
        self.assertEqual(res["path"], ["S4", "S6"])
        self.assertEqual(self.session.ap, 11)

    def test_complete_playthrough_1000_score(self):
        """
        Playthrough of Case 01 that reaches 1000+ score:
        1. Explore L1 (-1 AP -> 11)
        2. Explore L2 (-1 AP -> 10)
        3. Explore L3 (-1 AP -> 9)
        4. Debunk C3 (+250 pts, AP stays 9)
        5. Explore L4 (-1 AP -> 8)
        6. Explore L5 (-1 AP -> 7)
        7. Query path S4->S6 (-1 AP -> 6)
        8. Check alibi S5 at 23:45 (-1 AP -> 5)
        9. Accuse: Culprit S4, Accomplice S2
           Score: Culprit (500) + Accomplice (250) + Debunk (250) + AP (5 * 50 = 250) = 1250!
        """
        self.session.explore_lead("L1")
        self.session.explore_lead("L2")
        self.session.explore_lead("L3")
        self.session.debunk_clue("C3")
        self.session.explore_lead("L4")
        self.session.explore_lead("L5")
        self.session.query_path("S4", "S6")
        self.session.check_alibi("S5", "23:45")

        verdict = self.session.submit_accusal(culprit_id="S4", accomplice_id="S2")
        self.assertTrue(verdict["is_solved"])
        self.assertTrue(verdict["is_culprit_correct"])
        self.assertTrue(verdict["is_accomplice_correct"])
        self.assertTrue(verdict["is_contradiction_debunked"])
        self.assertGreaterEqual(verdict["score"], 1000)
        self.assertEqual(verdict["rank"], "Master Algorithmic Sleuth (O(1) Precision)")

if __name__ == "__main__":
    unittest.main()
