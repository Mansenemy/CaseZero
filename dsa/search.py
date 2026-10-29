"""
Searching Algorithms for CaseZero:
1. TimelineBinarySearch: O(log N) search over chronological security logs to verify alibis,
   returning a step-by-step trace of low, mid, and high pointers for UI visualization.
2. EvidenceTrie: Prefix tree supporting fast autocomplete and search across suspect traits,
   clues, and forensic tags.
"""

class TimelineBinarySearch:
    """
    Binary search engine for chronological security access logs.
    """

    @staticmethod
    def time_to_minutes(time_str: str) -> int:
        """Converts 'HH:MM' string to minutes from midnight."""
        try:
            h, m = map(int, time_str.split(":"))
            return h * 60 + m
        except Exception:
            return 0

    @classmethod
    def search(cls, sorted_logs: list[dict], target_time: str) -> dict:
        """
        Executes Binary Search on sorted security logs to find or bracket an event at target_time.
        Time complexity: O(log N).
        Space complexity: O(log N) for step trace.
        """
        target_min = cls.time_to_minutes(target_time)
        low = 0
        high = len(sorted_logs) - 1
        steps = []

        while low <= high:
            mid = (low + high) // 2
            mid_log = sorted_logs[mid]
            mid_min = cls.time_to_minutes(mid_log["time"])

            step_entry = {
                "step": len(steps) + 1,
                "low": low,
                "mid": mid,
                "high": high,
                "mid_time": mid_log["time"],
                "mid_event": mid_log.get("event", ""),
                "target_time": target_time
            }

            if mid_min == target_min:
                step_entry["comparison"] = "MATCH"
                steps.append(step_entry)

                # Collect all records sharing this exact timestamp (duplicate times)
                all_matching = [mid_log]
                # scan left
                l = mid - 1
                while l >= 0 and cls.time_to_minutes(sorted_logs[l]["time"]) == target_min:
                    all_matching.insert(0, sorted_logs[l])
                    l -= 1
                # scan right
                r = mid + 1
                while r < len(sorted_logs) and cls.time_to_minutes(sorted_logs[r]["time"]) == target_min:
                    all_matching.append(sorted_logs[r])
                    r += 1

                return {
                    "found": True,
                    "index": mid,
                    "item": mid_log,
                    "matching_items": all_matching,
                    "steps": steps,
                    "iterations": len(steps)
                }
            elif mid_min < target_min:
                step_entry["comparison"] = f"{mid_log['time']} < {target_time} (Move LOW -> {mid + 1})"
                steps.append(step_entry)
                low = mid + 1
            else:
                step_entry["comparison"] = f"{mid_log['time']} > {target_time} (Move HIGH -> {mid - 1})"
                steps.append(step_entry)
                high = mid - 1

        nearest_idx = min(max(0, low), len(sorted_logs) - 1) if sorted_logs else -1
        nearest_item = sorted_logs[nearest_idx] if nearest_idx >= 0 else None

        return {
            "found": False,
            "index": nearest_idx,
            "item": nearest_item,
            "steps": steps,
            "iterations": len(steps)
        }


class TrieNode:
    """Node in the EvidenceTrie."""
    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.is_end = False
        self.records = []  # list of dicts: {'id': ..., 'type': ..., 'text': ...}


class EvidenceTrie:
    """
    Prefix tree (Trie) for indexing and searching suspect traits, evidence notes, and alibis.
    """

    def __init__(self):
        self.root = TrieNode()
        self.word_count = 0

    def insert(self, word: str, record: dict) -> None:
        """
        Inserts a word and its record reference into the Trie.
        Time complexity: O(L) where L is length of word.
        """
        if not word:
            return
        clean_word = word.strip().lower()
        curr = self.root

        for char in clean_word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]

        if not curr.is_end:
            curr.is_end = True
            self.word_count += 1

        # Avoid duplicate records
        if not any(r.get("id") == record.get("id") and r.get("type") == record.get("type") for r in curr.records):
            curr.records.append(record)

    def autocomplete(self, prefix: str, max_results: int = 8) -> list[dict]:
        """
        Finds all records matching the given prefix.
        Time complexity: O(P + K) where P is prefix length and K is total matching characters.
        """
        if not prefix:
            return []

        clean_prefix = prefix.strip().lower()
        curr = self.root

        for char in clean_prefix:
            if char not in curr.children:
                return []
            curr = curr.children[char]

        results = []
        self._collect_words(curr, clean_prefix, results, max_results)
        return results

    def _collect_words(self, node: TrieNode, current_word: str, results: list, max_results: int) -> None:
        if len(results) >= max_results:
            return

        if node.is_end:
            for rec in node.records:
                results.append({
                    "word": current_word,
                    "record": rec
                })
                if len(results) >= max_results:
                    return

        for char in sorted(node.children.keys()):
            self._collect_words(node.children[char], current_word + char, results, max_results)
