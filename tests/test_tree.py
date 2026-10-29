"""
Unit Tests for InvestigationTree.
Verifies:
- N-ary lead hierarchy and node instantiation
- Prerequisite-based unlock mechanics
- Pre-Order (DFS) traversal for Deep Dive
- Level-Order (BFS) traversal for Broad Survey
- Lead exploration and AP deduction
- Subtree pruning
"""

import unittest
from dsa.tree import TreeNode, InvestigationTree

class TestInvestigationTree(unittest.TestCase):
    def setUp(self):
        self.root = TreeNode("ROOT", "Ground Zero", "SCENE", "Vault scene", ap_cost=0)
        self.l1 = TreeNode("L1", "Dust Keypad", "FORENSICS", "Dust terminal", ap_cost=1, clues=["C1"], prerequisites=["ROOT"])
        self.l2 = TreeNode("L2", "Airlock Firmware", "CYBER", "Extract logs", ap_cost=1, clues=["C2"], prerequisites=["L1"])
        self.l3 = TreeNode("L3", "Incident Desk", "INTERROGATION", "Read log", ap_cost=1, clues=["C3"], prerequisites=["ROOT"])

        self.root.add_child(self.l1)
        self.l1.add_child(self.l2)
        self.root.add_child(self.l3)

        self.tree = InvestigationTree(self.root)

    def test_initial_unlock_state(self):
        # ROOT is resolved, so L1 and L3 (prereq: ROOT) should be AVAILABLE
        self.assertEqual(self.l1.status, "AVAILABLE")
        self.assertEqual(self.l3.status, "AVAILABLE")
        # L2 requires L1 to be resolved, so it must be LOCKED
        self.assertEqual(self.l2.status, "LOCKED")

    def test_explore_lead_unlocks_child(self):
        res = self.tree.explore_lead("L1", current_ap=5)
        self.assertTrue(res["success"])
        self.assertEqual(self.l1.status, "RESOLVED")

        self.tree.update_unlocks({"ROOT", "L1"})
        self.assertEqual(self.l2.status, "AVAILABLE")

    def test_insufficient_ap(self):
        res = self.tree.explore_lead("L1", current_ap=0)
        self.assertFalse(res["success"])
        self.assertIn("Insufficient Action Points", res["message"])

    def test_pre_order_traversal(self):
        # Pre-order: ROOT, L1, L2, L3
        pre = self.tree.pre_order_traversal()
        order = [n["id"] for n in pre]
        self.assertEqual(order, ["ROOT", "L1", "L2", "L3"])

    def test_level_order_traversal(self):
        # Level-order: ROOT (lvl 0), L1 (lvl 1), L3 (lvl 1), L2 (lvl 2)
        lvl = self.tree.level_order_traversal()
        order = [n["id"] for n in lvl]
        self.assertEqual(order, ["ROOT", "L1", "L3", "L2"])

    def test_prune(self):
        self.assertTrue(self.tree.prune("L3"))
        self.assertIsNone(self.tree.find_node("L3"))
        # Root now has only 1 child (L1)
        self.assertEqual(len(self.root.children), 1)

if __name__ == "__main__":
    unittest.main()
