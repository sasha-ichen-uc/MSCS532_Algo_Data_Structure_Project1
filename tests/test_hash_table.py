"""Tests for ChainingHashTable."""

import unittest
from src.hash_table import ChainingHashTable


class TestChainingHashTable(unittest.TestCase):

    def setUp(self):
        self.ht = ChainingHashTable()

    def test_insert_and_lookup(self):
        self.ht.insert("key1", "value1")
        self.assertEqual(self.ht.lookup("key1"), "value1")

    def test_lookup_missing_key(self):
        self.assertIsNone(self.ht.lookup("nonexistent"))

    def test_update_existing_key(self):
        self.ht.insert("key1", "old")
        self.ht.insert("key1", "new")
        self.assertEqual(self.ht.lookup("key1"), "new")
        self.assertEqual(self.ht.size, 1)

    def test_delete(self):
        self.ht.insert("key1", "value1")
        self.assertTrue(self.ht.delete("key1"))
        self.assertIsNone(self.ht.lookup("key1"))
        self.assertEqual(self.ht.size, 0)

    def test_delete_nonexistent(self):
        self.assertFalse(self.ht.delete("ghost"))

    def test_collision_handling(self):
        # Force small capacity to guarantee collisions
        ht = ChainingHashTable(capacity=2)
        ht.insert("a", 1)
        ht.insert("b", 2)
        ht.insert("c", 3)
        self.assertEqual(ht.lookup("a"), 1)
        self.assertEqual(ht.lookup("b"), 2)
        self.assertEqual(ht.lookup("c"), 3)

    def test_auto_resize(self):
        ht = ChainingHashTable(capacity=4)
        for i in range(20):
            ht.insert(f"key{i}", i)
        self.assertGreater(ht.capacity, 4)
        # All values should still be retrievable after resize
        for i in range(20):
            self.assertEqual(ht.lookup(f"key{i}"), i)

    def test_load_factor(self):
        ht = ChainingHashTable(capacity=10)
        for i in range(5):
            ht.insert(i, i)
        self.assertAlmostEqual(ht.load_factor, 0.5)

    def test_keys_iterator(self):
        for i in range(5):
            self.ht.insert(f"k{i}", i)
        keys = set(self.ht.keys())
        self.assertEqual(keys, {"k0", "k1", "k2", "k3", "k4"})

    def test_tuple_keys_for_flow_tracking(self):
        flow1 = (167772161, 167772162)  # (10.0.0.1, 10.0.0.2)
        flow2 = (167772162, 167772161)
        self.ht.insert(flow1, {"packets": 10})
        self.ht.insert(flow2, {"packets": 5})
        self.assertEqual(self.ht.lookup(flow1)["packets"], 10)
        self.assertEqual(self.ht.lookup(flow2)["packets"], 5)

    def test_delete_from_chain_middle(self):
        ht = ChainingHashTable(capacity=1)  # all collide
        ht.insert("a", 1)
        ht.insert("b", 2)
        ht.insert("c", 3)
        self.assertTrue(ht.delete("b"))
        self.assertIsNone(ht.lookup("b"))
        self.assertEqual(ht.lookup("a"), 1)
        self.assertEqual(ht.lookup("c"), 3)


if __name__ == "__main__":
    unittest.main()
