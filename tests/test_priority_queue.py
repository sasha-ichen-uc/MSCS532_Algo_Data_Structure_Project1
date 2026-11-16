"""Tests for MinHeap priority queue."""

import unittest
from src.priority_queue import MinHeap


class TestMinHeap(unittest.TestCase):

    def setUp(self):
        self.heap = MinHeap()

    def test_enqueue_dequeue_single(self):
        self.heap.enqueue("pkt", 3)
        self.assertEqual(self.heap.dequeue(), "pkt")

    def test_priority_ordering(self):
        self.heap.enqueue("low", 7)
        self.heap.enqueue("high", 0)
        self.heap.enqueue("med", 3)
        self.assertEqual(self.heap.dequeue(), "high")
        self.assertEqual(self.heap.dequeue(), "med")
        self.assertEqual(self.heap.dequeue(), "low")

    def test_fifo_within_same_priority(self):
        self.heap.enqueue("first", 5)
        self.heap.enqueue("second", 5)
        self.heap.enqueue("third", 5)
        self.assertEqual(self.heap.dequeue(), "first")
        self.assertEqual(self.heap.dequeue(), "second")
        self.assertEqual(self.heap.dequeue(), "third")

    def test_peek(self):
        self.heap.enqueue("a", 2)
        self.heap.enqueue("b", 1)
        self.assertEqual(self.heap.peek(), "b")
        self.assertEqual(len(self.heap), 2)  # peek doesn't remove

    def test_dequeue_empty_raises(self):
        with self.assertRaises(IndexError):
            self.heap.dequeue()

    def test_peek_empty_raises(self):
        with self.assertRaises(IndexError):
            self.heap.peek()

    def test_is_empty(self):
        self.assertTrue(self.heap.is_empty())
        self.heap.enqueue("x", 0)
        self.assertFalse(self.heap.is_empty())
        self.heap.dequeue()
        self.assertTrue(self.heap.is_empty())

    def test_len(self):
        self.assertEqual(len(self.heap), 0)
        for i in range(10):
            self.heap.enqueue(f"p{i}", i)
        self.assertEqual(len(self.heap), 10)

    def test_mixed_insert_and_remove(self):
        self.heap.enqueue("a", 5)
        self.heap.enqueue("b", 1)
        self.assertEqual(self.heap.dequeue(), "b")
        self.heap.enqueue("c", 3)
        self.heap.enqueue("d", 0)
        self.assertEqual(self.heap.dequeue(), "d")
        self.assertEqual(self.heap.dequeue(), "c")
        self.assertEqual(self.heap.dequeue(), "a")

    def test_large_batch(self):
        import random
        items = list(range(100))
        random.shuffle(items)
        for val in items:
            self.heap.enqueue(val, val)
        result = [self.heap.dequeue() for _ in range(100)]
        self.assertEqual(result, list(range(100)))


if __name__ == "__main__":
    unittest.main()
