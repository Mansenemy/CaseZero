"""
In-Memory Game Session Manager for CaseZero.
Coordinates all Data Structures & Algorithms:
- CustomHashMap: Core store for suspect dossiers and clue records
- SuspectGraph: Suspect relationships, BFS shortest path, Connected Components
- SuspectSetEngine: Set difference, intersection, and contradiction detection
- InvestigationTree: N-ary lead hierarchy, deep dive vs broad survey
- TimelineBinarySearch & EvidenceTrie: O(log N) alibi verification & autocomplete
"""

from dsa.hashmap import CustomHashMap
from dsa.graph import SuspectGraph
from dsa.sets_engine import SuspectSetEngine
from dsa.tree import TreeNode, InvestigationTree
from dsa.search import TimelineBinarySearch, EvidenceTrie
from game.scoring import calculate_verdict
from game.cases import CASES
from game.generator import generate_procedural_case

class GameSession:
    """
    Active gameplay session managing player resources and DSA instances.
    """

    def __init__(self):
        self.case_data = None
        self.ap = 12
        self.max_ap = 12
        self.hints_used = 0
        self.max_hints = 2
        self.status = "PLAYING"  # PLAYING, SOLVED, FAILED

        # Core DSA instances
        self.suspect_map = CustomHashMap(16)
        self.clue_map = CustomHashMap(16)
        self.graph = SuspectGraph()
        self.sets = SuspectSetEngine()
        self.tree = None
        self.trie = EvidenceTrie()

        # Session tracking
        self.discovered_clues = []
        self.debunked_clues = set()
        self.explored_leads = set()
        self.last_search_trace = None
        self.verdict = None

    def start_case(self, case_id: str = "case_1", seed: int = None) -> dict:
        """
        Initializes a case session from catalog or procedural generator.
        """
        if case_id == "procedural" or case_id.startswith("procedural_"):
            case_data = generate_procedural_case(seed)
        else:
            case_data = CASES.get(case_id, CASES["case_1"])

        self.case_data = case_data
        self.ap = 12
        self.max_ap = 12
        self.hints_used = 0
        self.status = "PLAYING"
        self.discovered_clues = []
        self.debunked_clues = set()
        self.explored_leads = {"ROOT", "P_ROOT", "OM_ROOT"}
        self.last_search_trace = None
        self.verdict = None

        # Reset DSA stores
        self.suspect_map = CustomHashMap(16)
        self.clue_map = CustomHashMap(16)
        self.graph = SuspectGraph()
        self.sets = SuspectSetEngine()
        self.trie = EvidenceTrie()

        # 1. Populate Suspects in CustomHashMap, Graph, Sets, and Trie
        suspect_ids = []
        for s in case_data["suspects"]:
            s_id = s["id"]
            suspect_ids.append(s_id)
            self.suspect_map.put(s_id, s)
            self.graph.add_node(s_id, s)

            # Index traits and names in Trie
            self.trie.insert(s["name"], {"id": s_id, "type": "SUSPECT", "field": "name"})
            self.trie.insert(s["role"], {"id": s_id, "type": "SUSPECT", "field": "role"})
            for trait in s.get("traits", []):
                self.trie.insert(trait, {"id": s_id, "type": "SUSPECT", "field": "trait"})

        self.sets.set_universe(suspect_ids)

        # 2. Populate Graph Connections
        for conn in case_data.get("connections", []):
            self.graph.add_edge(conn["u"], conn["v"], conn["type"], conn.get("desc", ""))

        # 3. Populate Clues in CustomHashMap and Sets
        for c in case_data.get("clues", []):
            c_id = c["id"]
            self.clue_map.put(c_id, c)
            self.sets.register_clue(
                c_id,
                c.get("allowed", []),
                c.get("title", ""),
                is_forged=c.get("is_forged", False),
                contradicts=c.get("contradicts", [])
            )
            self.trie.insert(c["title"], {"id": c_id, "type": "CLUE", "field": "title"})

        # 4. Build Investigation Tree
        self._build_tree(case_data["tree"])

        return self.to_dict()

    def _build_tree(self, tree_data: dict) -> None:
        def build_node(d: dict) -> TreeNode:
            node = TreeNode(
                node_id=d["id"],
                title=d["title"],
                category=d.get("category", "SCENE"),
                description=d.get("description", ""),
                ap_cost=d.get("ap_cost", 1),
                clues=d.get("clues", []),
                prerequisites=d.get("prerequisites", [])
            )
            for ch in d.get("children", []):
                node.add_child(build_node(ch))
            return node

        root = build_node(tree_data)
        self.tree = InvestigationTree(root)

    def explore_lead(self, lead_id: str) -> dict:
        """
        Explores an investigation lead, deducting AP and discovering clues.
        """
        if self.status != "PLAYING":
            return {"success": False, "message": "Case already concluded."}

        node = self.tree.find_node(lead_id)
        if not node:
            return {"success": False, "message": "Lead does not exist."}

        if node.status != "AVAILABLE":
            return {"success": False, "message": f"Lead is {node.status}."}

        if self.ap < node.ap_cost:
            return {"success": False, "message": f"Need {node.ap_cost} AP, but only have {self.ap} AP."}

        self.ap -= node.ap_cost
        node.status = "RESOLVED"
        self.explored_leads.add(lead_id)
        self.tree.update_unlocks(self.explored_leads)

        new_clues = []
        for c_id in node.clues:
            if c_id not in self.discovered_clues:
                self.discovered_clues.append(c_id)
                clue_data = self.clue_map.get(c_id)
                if clue_data:
                    new_clues.append(clue_data)

        return {
            "success": True,
            "message": f"Explored: {node.title}",
            "ap_spent": node.ap_cost,
            "new_clues": new_clues,
            "session": self.to_dict()
        }

    def debunk_clue(self, clue_id: str) -> dict:
        """
        Attempts to debunk a suspected forgery.
        If correct, marks debunked and restores suspect set.
        If incorrect, penalizes 1 AP and gives a warning.
        """
        if self.status != "PLAYING":
            return {"success": False, "message": "Case already concluded."}

        clue = self.clue_map.get(clue_id)
        if not clue:
            return {"success": False, "message": "Clue not found."}

        is_actual_forgery = clue.get("is_forged", False)

        if is_actual_forgery:
            self.debunked_clues.add(clue_id)
            self.sets.debunk(clue_id)
            # If clue had an accomplice author, debunk edge
            return {
                "success": True,
                "is_forged": True,
                "message": f"Forgery exposed! Clue [{clue_id}] was fabricated and has been debunked.",
                "session": self.to_dict()
            }
        else:
            self.ap = max(0, self.ap - 1)
            return {
                "success": False,
                "is_forged": False,
                "message": f"False assertion! Clue [{clue_id}] is verified physical evidence. Lost 1 AP.",
                "session": self.to_dict()
            }

    def query_path(self, start: str, target: str) -> dict:
        """
        Runs BFS shortest path between two suspects. Costs 1 AP.
        """
        if self.status != "PLAYING":
            return {"success": False, "message": "Case already concluded."}

        if self.ap < 1:
            return {"success": False, "message": "Insufficient AP for path query."}

        self.ap -= 1
        res = self.graph.bfs_shortest_path(start, target)
        return {
            "success": True,
            "path": res["path"],
            "edges": res["edges"],
            "steps": res["steps"],
            "found": res["found"],
            "remaining_ap": self.ap
        }

    def check_alibi(self, suspect_id: str, target_time: str = "23:45") -> dict:
        """
        Executes Binary Search on sorted security access logs. Costs 1 AP.
        """
        if self.status != "PLAYING":
            return {"success": False, "message": "Case already concluded."}

        if self.ap < 1:
            return {"success": False, "message": "Insufficient AP for alibi check."}

        self.ap -= 1
        sorted_logs = sorted(self.case_data.get("security_logs", []), key=lambda x: x["time"])
        res = TimelineBinarySearch.search(sorted_logs, target_time)
        self.last_search_trace = res

        # Check if any found log at this timestamp belongs to suspect
        found_item = res.get("item")
        matching_items = res.get("matching_items", [found_item] if found_item else [])
        alibi_broken = False
        alibi_holds = False
        summary = ""

        # Prioritize log for this specific suspect if multiple exist at same time
        suspect_item = next((it for it in matching_items if it and it.get("suspect_id") == suspect_id), None)
        active_item = suspect_item if suspect_item else found_item

        if res["found"] and active_item:
            if active_item.get("suspect_id") == suspect_id:
                ev = active_item.get("event", "")
                loc = active_item.get("location", "")
                if "ALIBI VERIFIED" in ev:
                    alibi_holds = True
                    summary = f"Alibi Holds: {suspect_id} was confirmed at {loc}."
                elif "CRITICAL" in ev or "CRIME" in ev:
                    alibi_broken = True
                    summary = f"Alibi Broken! {suspect_id} caught breaching security at {loc}."
                else:
                    summary = f"Activity logged: {ev} at {loc}."
            else:
                summary = f"Timestamp logged for {active_item.get('suspect_id')} at {active_item.get('location')}."
        else:
            summary = "No security record at this exact timestamp."

        return {
            "success": True,
            "trace": res,
            "alibi_broken": alibi_broken,
            "alibi_holds": alibi_holds,
            "summary": summary,
            "remaining_ap": self.ap
        }

    def toggle_suspect(self, suspect_id: str) -> dict:
        """Toggles manual elimination of a suspect. Free."""
        if suspect_id in self.sets.manual_eliminated:
            self.sets.restore(suspect_id)
        else:
            self.sets.eliminate(suspect_id)
        return self.to_dict()

    def get_hint(self) -> dict:
        """Spends 2 AP for an investigative hint (max 2)."""
        if self.hints_used >= self.max_hints:
            return {"success": False, "message": "Maximum hints already used."}
        if self.ap < 2:
            return {"success": False, "message": "Need 2 AP to unlock a hint."}

        self.ap -= 2
        self.hints_used += 1

        hints = [
            f"Check the contradiction between thermal silhouette and guard statement.",
            f"Run an alibi check around 23:45 to test if the joint alibi holds."
        ]
        hint_text = hints[(self.hints_used - 1) % len(hints)]

        return {
            "success": True,
            "hint": hint_text,
            "hints_used": self.hints_used,
            "remaining_ap": self.ap
        }

    def submit_accusal(self, culprit_id: str, accomplice_id: str = "") -> dict:
        """
        Submits player's final indictment and computes verdict and score.
        """
        actual_culprit = self.case_data.get("culprit_id")
        actual_accomplice = self.case_data.get("accomplice_id")
        contradiction_debunked = self.case_data.get("forged_clue_id") in self.debunked_clues

        verdict = calculate_verdict(
            culprit_guess=culprit_id,
            accomplice_guess=accomplice_id,
            actual_culprit=actual_culprit,
            actual_accomplice=actual_accomplice,
            contradiction_debunked=contradiction_debunked,
            remaining_ap=self.ap
        )

        self.status = "SOLVED" if verdict["is_solved"] else "FAILED"
        self.verdict = verdict
        return verdict

    def get_under_the_hood(self, tab: str, suspect_id: str = None) -> dict:
        """
        Generates slim 3-line Under-the-Hood drawer statistics for active tab.
        """
        if tab == "suspects":
            stats = self.suspect_map.stats()
            return {
                "name": "Custom HashMap (djb2 Separate Chaining)",
                "explanation": "Dossiers are retrieved in O(1) average time via polynomial rolling hash.",
                "complexity": "O(1) Avg",
                "visual_type": "hashmap",
                "data": {
                    "capacity": stats["capacity"],
                    "size": stats["size"],
                    "load_factor": stats["load_factor"],
                    "collisions": stats["collisions"],
                    "last_accessed": stats["last_accessed_bucket"],
                    "buckets": [b["chain_length"] for b in stats["buckets"]]
                }
            }
        elif tab == "connections":
            target_id = suspect_id or (self.case_data["suspects"][0]["id"] if self.case_data else "")
            neighbors = self.graph.get_neighbors(target_id)
            comps = self.graph.connected_components()
            return {
                "name": "Suspect Graph (Adjacency List & Matrix)",
                "explanation": "BFS traces collusion chains across suspect network in O(V + E) time.",
                "complexity": "O(V + E)",
                "visual_type": "graph",
                "data": {
                    "selected_node": target_id,
                    "neighbor_count": len(neighbors),
                    "syndicate_count": len(comps),
                    "neighbors": [f"{e['target']} ({e['type']})" for e in neighbors]
                }
            }
        elif tab == "evidence":
            res = self.sets.compute_viable(self.discovered_clues)
            return {
                "name": "Suspect Set Theory (Universe \\ Eliminated ∩ Clues)",
                "explanation": "Mathematical intersections filter suspects and expose empty set contradictions.",
                "complexity": "O(C · U)",
                "visual_type": "sets",
                "data": {
                    "universe_count": len(res["universe"]),
                    "eliminated_count": len(res["eliminated"]),
                    "viable_count": len(res["viable"])
                }
            }
        elif tab == "leads":
            pre = self.tree.pre_order_traversal() if self.tree else []
            lvl = self.tree.level_order_traversal() if self.tree else []
            return {
                "name": "Investigation Decision Tree",
                "explanation": "Tree traversal coordinates Deep Dive (DFS) and Broad Survey (BFS) inquiry.",
                "complexity": "O(N)",
                "visual_type": "tree",
                "data": {
                    "pre_order_ids": [n["id"] for n in pre],
                    "level_order_ids": [n["id"] for n in lvl]
                }
            }
        elif tab == "alibi":
            last_trace = self.last_search_trace or {"steps": [], "iterations": 0}
            return {
                "name": "Timeline Binary Search",
                "explanation": "Logarithmically checks chronological access logs in O(log N) steps.",
                "complexity": "O(log N)",
                "visual_type": "search",
                "data": {
                    "steps": last_trace.get("steps", []),
                    "iterations": last_trace.get("iterations", 0)
                }
            }
        return {
            "name": "Data Structures & Algorithms",
            "explanation": "Core algorithmic engine driving investigative forensic logic.",
            "complexity": "O(1)",
            "visual_type": "none",
            "data": {}
        }

    def to_dict(self) -> dict:
        """
        Serializes full state snapshot for API / GUI consumption.
        """
        if not self.case_data:
            return {}

        active_clues = [c for c in self.discovered_clues if c not in self.debunked_clues]
        set_result = self.sets.compute_viable(self.discovered_clues)

        suspects_list = []
        for s in self.case_data.get("suspects", []):
            s_copy = dict(s)
            s_copy["is_viable"] = s["id"] in set_result["viable"]
            s_copy["is_eliminated"] = s["id"] in set_result["eliminated"]
            suspects_list.append(s_copy)

        discovered_clues_list = []
        for c_id in self.discovered_clues:
            c_data = self.clue_map.get(c_id)
            if c_data:
                c_copy = dict(c_data)
                c_copy["debunked"] = c_id in self.debunked_clues
                discovered_clues_list.append(c_copy)

        return {
            "case_id": self.case_data.get("id"),
            "case_title": self.case_data.get("title"),
            "case_location": self.case_data.get("location"),
            "briefing": self.case_data.get("briefing"),
            "scene_image": self.case_data.get("scene_image"),
            "ap": self.ap,
            "max_ap": self.max_ap,
            "hints_used": self.hints_used,
            "status": self.status,
            "suspects": suspects_list,
            "viable_suspect_ids": sorted(list(set_result["viable"])),
            "eliminated_suspect_ids": sorted(list(set_result["eliminated"])),
            "contradiction_detected": set_result["contradiction"],
            "conflicting_clues": set_result["conflicting_clues"],
            "set_steps": set_result["steps"],
            "discovered_clues": discovered_clues_list,
            "connections": self.case_data.get("connections", []),
            "tree": self.tree.root.to_dict() if self.tree and self.tree.root else None,
            "security_logs": sorted(self.case_data.get("security_logs", []), key=lambda x: x["time"]),
            "verdict": self.verdict
        }
