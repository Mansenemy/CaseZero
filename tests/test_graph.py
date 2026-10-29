"""
Unit Tests for SuspectGraph.
Verifies:
- Node and typed edge additions
- Edge debunking
- BFS shortest path calculation (O(V + E))
- Connected Components detection (syndicates)
- 2D Adjacency Matrix structure
"""

import unittest
from dsa.graph import SuspectGraph

class TestSuspectGraph(unittest.TestCase):
    def setUp(self):
        self.graph = SuspectGraph()
        for i in range(1, 7):
            self.graph.add_node(f"S{i}")

        self.graph.add_edge("S1", "S2", "COLLEAGUE")
        self.graph.add_edge("S2", "S4", "CONSPIRACY")
        self.graph.add_edge("S3", "S4", "EQUIPMENT")
        self.graph.add_edge("S3", "S6", "DEBT")
        self.graph.add_edge("S5", "S2", "COLLEAGUE")

    def test_neighbors(self):
        nbrs = self.graph.get_neighbors("S2")
        targets = {e["target"] for e in nbrs}
        self.assertEqual(targets, {"S1", "S4", "S5"})

    def test_debunk_edge(self):
        self.graph.debunk_edge("S2", "S5")
        active_nbrs = self.graph.get_neighbors("S2", include_debunked=False)
        targets = {e["target"] for e in active_nbrs}
        self.assertNotIn("S5", targets)
        self.assertIn("S1", targets)

        all_nbrs = self.graph.get_neighbors("S2", include_debunked=True)
        all_targets = {e["target"] for e in all_nbrs}
        self.assertIn("S5", all_targets)

    def test_bfs_shortest_path(self):
        # S1 -> S2 -> S4 -> S3 -> S6
        res = self.graph.bfs_shortest_path("S1", "S6")
        self.assertTrue(res["found"])
        self.assertEqual(res["path"], ["S1", "S2", "S4", "S3", "S6"])
        self.assertEqual(len(res["edges"]), 4)

    def test_bfs_no_path(self):
        isolated_graph = SuspectGraph()
        isolated_graph.add_node("A")
        isolated_graph.add_node("B")
        res = isolated_graph.bfs_shortest_path("A", "B")
        self.assertFalse(res["found"])
        self.assertEqual(res["path"], [])

    def test_connected_components(self):
        # S1, S2, S3, S4, S5, S6 are all in 1 connected component
        comps = self.graph.connected_components()
        self.assertEqual(len(comps), 1)
        self.assertEqual(len(comps[0]), 6)

        # Add isolated node
        self.graph.add_node("ISO")
        comps2 = self.graph.connected_components()
        self.assertEqual(len(comps2), 2)

    def test_adjacency_matrix(self):
        mat_data = self.graph.adjacency_matrix()
        self.assertEqual(len(mat_data["node_ids"]), 6)
        matrix = mat_data["matrix"]
        self.assertEqual(len(matrix), 6)
        self.assertEqual(len(matrix[0]), 6)

if __name__ == "__main__":
    unittest.main()
