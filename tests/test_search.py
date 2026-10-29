"""
Unit Tests for Searching Algorithms:
- TimelineBinarySearch: O(log N) search on chronological logs + step trace
- EvidenceTrie: Prefix tree insert + autocomplete
"""

import unittest
from dsa.search import TimelineBinarySearch, EvidenceTrie

class TestSearchingAlgorithms(unittest.TestCase):
    def setUp(self):
        self.logs = [
            {"time": "19:40", "suspect_id": "S4", "event": "Lobby tap"},
            {"time": "20:15", "suspect_id": "S1", "event": "Login"},
            {"time": "21:30", "suspect_id": "S3", "event": "Sublevel 1"},
            {"time": "22:15", "suspect_id": "S2", "event": "Override"},
            {"time": "23:45", "suspect_id": "S5", "event": "Grant signed"},
            {"time": "23:45", "suspect_id": "S4", "event": "Vault breached"},
            {"time": "00:05", "suspect_id": "S4", "event": "Exit bay"}
        ]
        self.sorted_logs = sorted(self.logs, key=lambda x: x["time"])

        self.trie = EvidenceTrie()
        self.trie.insert("Dr. Aris Thorne", {"id": "S1", "type": "SUSPECT"})
        self.trie.insert("Thermal camera", {"id": "C5", "type": "CLUE"})
        self.trie.insert("Terminal access", {"id": "L1", "type": "LEAD"})
        self.trie.insert("Left-Handed", {"id": "S1", "type": "TRAIT"})

    def test_binary_search_found(self):
        res = TimelineBinarySearch.search(self.sorted_logs, "21:30")
        self.assertTrue(res["found"])
        self.assertEqual(res["item"]["time"], "21:30")
        self.assertEqual(res["item"]["suspect_id"], "S3")
        self.assertGreater(len(res["steps"]), 0)
        # Verify step trace pointers
        first_step = res["steps"][0]
        self.assertEqual(first_step["low"], 0)
        self.assertEqual(first_step["high"], len(self.sorted_logs) - 1)

    def test_binary_search_not_found(self):
        res = TimelineBinarySearch.search(self.sorted_logs, "21:00")
        self.assertFalse(res["found"])
        self.assertIsNotNone(res["item"])
        self.assertGreater(len(res["steps"]), 0)

    def test_trie_autocomplete_matches(self):
        res = self.trie.autocomplete("Th")
        # Should match 'Thermal camera' and 'Dr. Aris Thorne' (case-insensitive)
        words = [m["word"] for m in res]
        self.assertTrue(any("thermal" in w for w in words))

    def test_trie_empty_or_no_match(self):
        self.assertEqual(self.trie.autocomplete(""), [])
        self.assertEqual(self.trie.autocomplete("XYZ123"), [])

if __name__ == "__main__":
    unittest.main()
