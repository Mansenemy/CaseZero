"""
Custom HashMap Implementation for CaseZero.
Implements the djb2 polynomial rolling hash algorithm with separate chaining collision resolution.
Meets strict DSA requirements:
- Average O(1) time complexity for put, get, and delete.
- Worst-case O(N) when multiple keys collide in the same bucket.
- Automatic resizing when load factor exceeds 0.75.
- stats() method returning bucket details, chain lengths, collision count, and load factor.
"""

class CustomHashMap:
    """
    A custom hash table using djb2 hashing and separate chaining.
    Used as the core storage for suspect dossiers and clue metadata.
    """

    def __init__(self, capacity: int = 16):
        """
        Initializes hash table with a power-of-two or prime capacity.
        Time complexity: O(capacity).
        """
        self.capacity = max(4, capacity)
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]
        self.collisions = 0
        self.last_accessed_bucket = None

    def _hash(self, key: str) -> int:
        """
        Classic djb2 string hashing algorithm.
        hash = hash * 33 + c
        Time complexity: O(L) where L is key length.
        """
        h = 5381
        for char in str(key):
            h = (((h << 5) + h) + ord(char)) & 0xFFFFFFFF
        return h % self.capacity

    def put(self, key: str, value: any) -> None:
        """
        Inserts or updates a key-value pair.
        Resizes if load factor exceeds 0.75.
        Time complexity: Average O(1), Worst O(N).
        """
        idx = self._hash(key)
        self.last_accessed_bucket = idx
        bucket = self.buckets[idx]

        for entry in bucket:
            if entry[0] == key:
                entry[1] = value
                return

        # If bucket already has elements, this insertion causes a collision
        if len(bucket) > 0:
            self.collisions += 1

        bucket.append([key, value])
        self.size += 1

        # Check load factor for dynamic resizing
        if (self.size / self.capacity) > 0.75:
            self._resize(self.capacity * 2)

    def get(self, key: str, default: any = None) -> any:
        """
        Retrieves the value for key, or returns default if not found.
        Time complexity: Average O(1), Worst O(N).
        """
        idx = self._hash(key)
        self.last_accessed_bucket = idx
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return default

    def contains(self, key: str) -> bool:
        """
        Checks if key exists in hash map.
        Time complexity: Average O(1).
        """
        return self.get(key) is not None

    def delete(self, key: str) -> bool:
        """
        Removes a key from the hash table.
        Time complexity: Average O(1), Worst O(N).
        """
        idx = self._hash(key)
        self.last_accessed_bucket = idx
        bucket = self.buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return True
        return False

    def _resize(self, new_capacity: int) -> None:
        """
        Doubles capacity and rehashes all elements.
        Time complexity: O(N + capacity).
        """
        old_buckets = self.buckets
        self.capacity = new_capacity
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        self.collisions = 0

        for bucket in old_buckets:
            for k, v in bucket:
                self.put(k, v)

    def keys(self) -> list:
        """Returns all keys in hash table."""
        res = []
        for bucket in self.buckets:
            for k, _ in bucket:
                res.append(k)
        return res

    def values(self) -> list:
        """Returns all values in hash table."""
        res = []
        for bucket in self.buckets:
            for _, v in bucket:
                res.append(v)
        return res

    def items(self) -> list:
        """Returns all (key, value) tuples."""
        res = []
        for bucket in self.buckets:
            for k, v in bucket:
                res.append((k, v))
        return res

    def stats(self) -> dict:
        """
        Returns live operational statistics for Under-the-Hood drawer.
        """
        load_factor = round(self.size / self.capacity, 3)
        bucket_details = []
        for idx, bucket in enumerate(self.buckets):
            bucket_details.append({
                "index": idx,
                "chain_length": len(bucket),
                "keys": [entry[0] for entry in bucket]
            })

        return {
            "capacity": self.capacity,
            "size": self.size,
            "load_factor": load_factor,
            "collisions": self.collisions,
            "last_accessed_bucket": self.last_accessed_bucket,
            "buckets": bucket_details
        }
