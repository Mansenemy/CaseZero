"""
Investigation Decision Tree for CaseZero.
Hierarchically structures crime scene leads into an n-ary decision tree:
- Nodes represent investigative actions (e.g. dusting keypad, decrypting telemetry).
- Prerequisites enforce logical progression (e.g. access server before decrypting logs).
- Pre-Order Traversal (DFS): Represents the "Deep Dive" forensic sequence.
- Level-Order Traversal (BFS): Represents the "Broad Survey" wide sweep sequence.
- Pruning: Allows branches to be pruned or flagged.
"""

from collections import deque

class TreeNode:
    """
    Individual lead node within the investigation tree.
    """

    def __init__(self, node_id: str, title: str, category: str, description: str,
                 ap_cost: int = 1, clues: list[str] = None, prerequisites: list[str] = None):
        """
        Initializes a lead node.
        Time complexity: O(1).
        """
        self.id = node_id
        self.title = title
        self.category = category  # SCENE, FORENSICS, CYBER, INTERROGATION, FINANCE
        self.description = description
        self.ap_cost = ap_cost
        self.clues = clues or []
        self.prerequisites = prerequisites or []
        self.status = "LOCKED"  # LOCKED, AVAILABLE, RESOLVED
        self.children = []
        self.parent_id = None

    def add_child(self, child_node: "TreeNode") -> None:
        """Adds child lead node and sets parent pointer."""
        child_node.parent_id = self.id
        self.children.append(child_node)

    def to_dict(self) -> dict:
        """Serializes node and children to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "description": self.description,
            "ap_cost": self.ap_cost,
            "clues": self.clues,
            "prerequisites": self.prerequisites,
            "status": self.status,
            "children": [c.to_dict() for c in self.children]
        }


class InvestigationTree:
    """
    N-ary tree structuring case leads and inquiries.
    """

    def __init__(self, root: TreeNode = None):
        """
        Initializes investigation tree.
        Root is ground zero scene (status=RESOLVED by default so level 1 leads are AVAILABLE).
        """
        self.root = root
        if self.root:
            self.root.status = "RESOLVED"
            self.update_unlocks({self.root.id})

    def find_node(self, target_id: str, curr: TreeNode = None) -> TreeNode | None:
        """
        Finds a node by ID using Depth-First Search.
        Time complexity: O(N) where N is total node count.
        """
        if curr is None:
            curr = self.root
        if not curr:
            return None
        if curr.id == target_id:
            return curr

        for child in curr.children:
            found = self.find_node(target_id, child)
            if found:
                return found
        return None

    def update_unlocks(self, explored_ids: set[str]) -> None:
        """
        Updates node unlock statuses based on satisfied prerequisites.
        Time complexity: O(N * P) where P is max prerequisites count.
        """
        def traverse(node: TreeNode):
            if not node:
                return
            if node.status != "RESOLVED":
                if not node.prerequisites or all(p in explored_ids for p in node.prerequisites):
                    node.status = "AVAILABLE"
                else:
                    node.status = "LOCKED"

            for child in node.children:
                traverse(child)

        traverse(self.root)

    def explore_lead(self, node_id: str, current_ap: int) -> dict:
        """
        Resolves a lead if available and AP is sufficient.
        Time complexity: O(N).
        """
        node = self.find_node(node_id)
        if not node:
            return {"success": False, "message": "Lead not found.", "cost": 0, "clues": []}

        if node.status != "AVAILABLE":
            return {"success": False, "message": f"Lead is currently {node.status}.", "cost": 0, "clues": []}

        if current_ap < node.ap_cost:
            return {"success": False, "message": "Insufficient Action Points (AP).", "cost": 0, "clues": []}

        node.status = "RESOLVED"
        return {"success": True, "message": f"Lead explored: {node.title}", "cost": node.ap_cost, "clues": node.clues}

    def pre_order_traversal(self) -> list[dict]:
        """
        Pre-Order Depth-First Traversal (Root -> Left -> Right).
        Represents Deep Dive investigative sequencing.
        Time complexity: O(N).
        """
        result = []

        def dfs(node: TreeNode, depth: int):
            if not node:
                return
            result.append({
                "id": node.id,
                "title": node.title,
                "category": node.category,
                "status": node.status,
                "ap_cost": node.ap_cost,
                "depth": depth
            })
            for child in node.children:
                dfs(child, depth + 1)

        dfs(self.root, 0)
        return result

    def level_order_traversal(self) -> list[dict]:
        """
        Level-Order Breadth-First Traversal (by depth level).
        Represents Broad Survey investigative sequencing.
        Time complexity: O(N).
        """
        if not self.root:
            return []

        result = []
        queue = deque([(self.root, 0)])

        while queue:
            node, level = queue.popleft()
            result.append({
                "id": node.id,
                "title": node.title,
                "category": node.category,
                "status": node.status,
                "ap_cost": node.ap_cost,
                "level": level
            })
            for child in node.children:
                queue.append((child, level + 1))

        return result

    def prune(self, node_id: str) -> bool:
        """
        Prunes a subtree branch rooted at node_id.
        Time complexity: O(N).
        """
        if not self.root or self.root.id == node_id:
            return False

        def search_and_remove(parent: TreeNode):
            for i, child in enumerate(parent.children):
                if child.id == node_id:
                    parent.children.pop(i)
                    return True
                if search_and_remove(child):
                    return True
            return False

        return search_and_remove(self.root)
