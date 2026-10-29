"""
Suspect Set Theory Engine for CaseZero.
Implements mathematical set operations to filter suspects and detect contradictions:
- Universe set (U): All suspects in the case
- Eliminated set (E): Suspects proven innocent or ruled out
- Clue constraint sets: Suspects permitted by specific forensic evidence
- Viable candidate calculation: Viable = (U \\ E) ∩ ⋂(Clue_Constraints)
- Contradiction Detection: Triggers when intersection results in the Empty Set (∅)
"""

class SuspectSetEngine:
    """
    Manages suspect elimination and logical contradiction alerts via Set Theory.
    """

    def __init__(self, universe: list[str] = None):
        """
        Initializes set engine with universe of suspect IDs.
        Time complexity: O(U) where U is universe size.
        """
        self.universe = set(universe or [])
        self.eliminated = set()
        self.manual_eliminated = set()
        self.clues = {}  # clue_id -> dict(allowed, title, is_forged, contradicts)

    def set_universe(self, suspect_ids: list[str]) -> None:
        """
        Sets universe of suspects.
        Time complexity: O(U).
        """
        self.universe = set(suspect_ids)
        self.eliminated.clear()
        self.manual_eliminated.clear()
        self.clues.clear()

    def register_clue(self, clue_id: str, allowed_suspects: list[str], title: str = "",
                      is_forged: bool = False, contradicts: list[str] = None) -> None:
        """
        Registers a clue with its permitted suspect subset.
        Time complexity: O(K) where K is size of allowed_suspects.
        """
        self.clues[clue_id] = {
            "allowed": set(allowed_suspects),
            "title": title or clue_id,
            "is_forged": is_forged,
            "debunked": False,
            "contradicts": contradicts or []
        }

    def eliminate(self, suspect_id: str) -> None:
        """
        Eliminates a suspect from the viable candidate pool.
        Time complexity: O(1).
        """
        if suspect_id in self.universe:
            self.manual_eliminated.add(suspect_id)

    def restore(self, suspect_id: str) -> None:
        """
        Restores a previously eliminated suspect.
        Time complexity: O(1).
        """
        self.manual_eliminated.discard(suspect_id)
        self.eliminated.discard(suspect_id)

    def debunk(self, clue_id: str) -> bool:
        """
        Debunks a forged or planted clue.
        Time complexity: O(1).
        """
        if clue_id in self.clues:
            self.clues[clue_id]["debunked"] = True
            return True
        return False

    def compute_viable(self, active_clue_ids: list[str]) -> dict:
        """
        Computes viable suspects via set difference and intersection:
        Viable = (Universe \\ Eliminated) ∩ ⋂(Clue_Constraints)
        Detects contradiction when intersection becomes empty (∅).

        Time complexity: O(C * U) where C is active clue count and U is universe size.
        """
        all_eliminated = self.eliminated.union(self.manual_eliminated)
        candidates = self.universe.difference(all_eliminated)

        steps = [
            f"1. Universe (U): {sorted(list(self.universe))}",
            f"2. Filter (U \\ E): {sorted(list(candidates))}"
        ]

        contradiction = False
        conflicting_clues = []
        applied_clues = []

        for c_id in active_clue_ids:
            clue = self.clues.get(c_id)
            if not clue or clue["debunked"]:
                continue

            applied_clues.append(c_id)
            allowed = clue["allowed"]
            next_intersection = candidates.intersection(allowed)

            # Contradiction Detection: If intersection is empty while candidates existed
            if len(next_intersection) == 0 and len(candidates) > 0:
                contradiction = True
                conflicting_clues = [c_id]
                # Find the opposing clue that caused conflict
                for prev_id in applied_clues[:-1]:
                    prev_clue = self.clues.get(prev_id)
                    if prev_clue and len(prev_clue["allowed"].intersection(allowed)) == 0:
                        conflicting_clues.insert(0, prev_id)
                        break
                if clue.get("contradicts"):
                    for c_target in clue["contradicts"]:
                        if c_target in active_clue_ids and c_target not in conflicting_clues:
                            conflicting_clues.insert(0, c_target)

                candidates = set()  # Empty set (∅) represents logical deadlock
                steps.append(
                    f"3. Intersect [{c_id}]: Candidates ∩ {sorted(list(allowed))} = ∅ (CONTRADICTION DETECTED!)"
                )
                break
            else:
                candidates = next_intersection
                steps.append(
                    f"3. Intersect [{c_id}]: {sorted(list(candidates))}"
                )

        return {
            "viable": candidates,
            "eliminated": all_eliminated,
            "universe": self.universe,
            "contradiction": contradiction,
            "conflicting_clues": conflicting_clues,
            "steps": steps
        }
