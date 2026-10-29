"""
Unit Tests for CustomHashMap.
Verifies:
- O(1) basic operations (put, get, contains, delete)
- Separate chaining collision handling
- Automatic resizing when load factor > 0.75
- stats() dictionary metrics
"""

import unittest
from dsa.hashmap import CustomHashMap

class TestCustomHashMap(unittest.TestCase):
    def setUp(self):
        self.map = CustomHashMap(capacity=8)

    def test_put_and_get(self):
        self.map.put("S1", {"name": "Dr. Aris Thorne"})
        self.map.put("S2", {"name": "Elena Vance"})
        self.assertEqual(self.map.get("S1")["name"], "Dr. Aris Thorne")
        self.assertEqual(self.map.get("S2")["name"], "Elena Vance")
        self.assertIsNone(self.map.get("UNKNOWN"))

    def test_update_existing_key(self):
        self.map.put("key", "initial")
        self.map.put("key", "updated")
        self.assertEqual(self.map.get("key"), "updated")
        self.assertEqual(self.map.size, 1)

    def test_delete(self):
        self.map.put("target", "value")
        self.assertTrue(self.map.contains("target"))
        self.assertTrue(self.map.delete("target"))
        self.assertFalse(self.map.contains("target"))
        self.assertFalse(self.map.delete("target"))

    def test_collisions_and_chaining(self):
        # Force multiple items into small map
        small_map = CustomHashMap(capacity=4)
        for i in range(10):
            small_map.put(f"item_{i}", i)

        for i in range(10):
            self.assertEqual(small_map.get(f"item_{i}"), i)

        stats = small_map.stats()
        self.assertGreater(stats["capacity"], 4)  # Must have resized!
        self.assertEqual(stats["size"], 10)

    def test_resize_trigger_at_load_factor(self):
        # Initial capacity 4. Threshold is 4 * 0.75 = 3
        test_map = CustomHashMap(capacity=4)
        test_map.put("k1", 1)
        test_map.put("k2", 2)
        test_map.put("k3", 3)
        self.assertEqual(test_map.capacity, 4)

        # 4th item triggers resize because 4/4 = 1.0 > 0.75
        test_map.put("k4", 4)
        self.assertGreater(test_map.capacity, 4)
        self.assertEqual(test_map.get("k1"), 1)
        self.assertEqual(test_map.get("k4"), 4)

    def test_stats_structure(self):
        self.map.put("test_key", "test_val")
        stats = self.map.stats()
        self.assertIn("capacity", stats)
        self.assertIn("size", stats)
        self.assertIn("load_factor", stats)
        self.assertIn("collisions", stats)
        self.assertIn("buckets", stats)
        self.assertEqual(len(stats["buckets"]), stats["capacity"])

if __name__ == "__main__":
    unittest.main()
