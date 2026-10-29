"""
Suspect Relationship Graph for CaseZero.
Represents relationships between suspects with typed edges:
- COLLEAGUE: Professional or department ties
- BLACKMAIL: Coercive leverage
- CONSPIRACY: Secret collaboration
- DEBT: Financial or gambling obligations
- EQUIPMENT: Exchange of bypass cards or tools

Provides:
- Adjacency List & 2D Adjacency Matrix representations
- Breadth-First Search (BFS) for shortest collusion paths (O(V + E))
- Connected Components for criminal syndicate detection (O(V + E))
"""

from collections import deque

class SuspectGraph:
    """
    Undirected graph representing suspects and their known connections.
    """

    VALID_EDGE_TYPES = {"COLLEAGUE", "BLACKMAIL", "CONSPIRACY", "DEBT", "EQUIPMENT"}

    def __init__(self):
        """
        Initializes empty graph.
        Time complexity: O(1).
        """
        self.adj = {}  # suspect_id -> list of edge dicts
        self.nodes = {}  # suspect_id -> suspect data

    def add_node(self, suspect_id: str, data: dict = None) -> None:
        """
        Adds suspect vertex to the graph.
        Time complexity: O(1).
        """
        if suspect_id not in self.nodes:
            self.nodes[suspect_id] = data or {"id": suspect_id}
            self.adj[suspect_id] = []

    def add_edge(self, u: str, v: str, rel_type: str, desc: str = "", weight: int = 1) -> bool:
        """
        Adds an undirected typed edge between suspect u and suspect v.
        Time complexity: O(deg(u) + deg(v)).
        """
        if u not in self.nodes or v not in self.nodes:
            return False

        rel_type = rel_type.upper()
        if rel_type not in self.VALID_EDGE_TYPES:
            rel_type = "COLLEAGUE"

        # Check existing edge to avoid duplicates
        for edge in self.adj[u]:
            if edge["target"] == v and edge["type"] == rel_type:
                return True

        self.adj[u].append({
            "target": v,
            "type": rel_type,
            "desc": desc,
            "weight": weight,
            "debunked": False
        })

        self.adj[v].append({
            "target": u,
            "type": rel_type,
            "desc": desc,
            "weight": weight,
            "debunked": False
        })
        return True

    def debunk_edge(self, u: str, v: str, rel_type: str = None) -> bool:
        """
        Marks an edge between u and v as debunked (e.g., false alibi or fabricated connection).
        Time complexity: O(deg(u) + deg(v)).
        """
        debunked_any = False
        for edge in self.adj.get(u, []):
            if edge["target"] == v and (rel_type is None or edge["type"] == rel_type):
                edge["debunked"] = True
                debunked_any = True

        for edge in self.adj.get(v, []):
            if edge["target"] == u and (rel_type is None or edge["type"] == rel_type):
                edge["debunked"] = True
                debunked_any = True

        return debunked_any

    def get_neighbors(self, suspect_id: str, include_debunked: bool = False) -> list:
        """
        Returns list of active neighbors for a suspect.
        Time complexity: O(deg(suspect_id)).
        """
        edges = self.adj.get(suspect_id, [])
        if include_debunked:
            return edges
        return [e for e in edges if not e["debunked"]]

    def bfs_shortest_path(self, start: str, target: str, include_debunked: bool = False) -> dict:
        """
        Executes Breadth-First Search (BFS) to identify the shortest connection chain
        between two suspects.
        Time complexity: O(V + E).
        Space complexity: O(V).
        """
        if start not in self.nodes or target not in self.nodes:
            return {"found": False, "path": [], "edges": [], "steps": 0}

        if start == target:
            return {"found": True, "path": [start], "edges": [], "steps": 0}

        queue = deque([start])
        visited = {start}
        parent_map = {}  # node -> (parent_node, edge_data)
        steps = 0

        while queue:
            curr = queue.popleft()
            steps += 1

            if curr == target:
                path = []
                edges = []
                trace = target
                while trace != start:
                    path.append(trace)
                    p_node, edge_data = parent_map[trace]
                    edges.append(edge_data)
                    trace = p_node
                path.append(start)
                path.reverse()
                edges.reverse()
                return {"found": True, "path": path, "edges": edges, "steps": steps}

            for edge in self.get_neighbors(curr, include_debunked):
                neighbor = edge["target"]
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent_map[neighbor] = (curr, edge)
                    queue.append(neighbor)

        return {"found": False, "path": [], "edges": [], "steps": steps}

    def connected_components(self, include_debunked: bool = False) -> list:
        """
        Identifies all isolated or interconnected clusters (syndicates).
        Time complexity: O(V + E).
        """
        visited = set()
        components = []

        for node_id in self.nodes:
            if node_id not in visited:
                comp = []
                queue = deque([node_id])
                visited.add(node_id)

                while queue:
                    curr = queue.popleft()
                    comp.append(curr)

                    for edge in self.get_neighbors(curr, include_debunked):
                        nbr = edge["target"]
                        if nbr not in visited:
                            visited.add(nbr)
                            queue.append(nbr)

                components.append(comp)

        return components

    def adjacency_matrix(self) -> dict:
        """
        Generates 2D Adjacency Matrix representation.
        Time complexity: O(V^2).
        """
        node_ids = sorted(list(self.nodes.keys()))
        index_map = {nid: i for i, nid in enumerate(node_ids)}
        size = len(node_ids)
        matrix = [[0] * size for _ in range(size)]

        for u in node_ids:
            u_idx = index_map[u]
            for edge in self.get_neighbors(u, include_debunked=False):
                v_idx = index_map[edge["target"]]
                matrix[u_idx][v_idx] = edge.get("weight", 1)

        return {
            "node_ids": node_ids,
            "matrix": matrix
        }
