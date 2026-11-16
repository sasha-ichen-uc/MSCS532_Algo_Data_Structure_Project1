"""Tests for BinaryTrie longest-prefix matching."""

import unittest
from src.trie import BinaryTrie
from src.packet import Packet


class TestBinaryTrie(unittest.TestCase):

    def setUp(self):
        self.trie = BinaryTrie()

    def test_insert_and_lookup_single_prefix(self):
        self.trie.insert_cidr("10.0.0.0/8", "iface-lan")
        self.assertEqual(self.trie.lookup_ip("10.5.5.5"), "iface-lan")

    def test_longest_prefix_match(self):
        self.trie.insert_cidr("10.0.0.0/8", "iface-lan")
        self.trie.insert_cidr("10.1.0.0/16", "iface-dept")
        self.trie.insert_cidr("10.1.1.0/24", "iface-lab")
        # Should match the /24, not the /16 or /8
        self.assertEqual(self.trie.lookup_ip("10.1.1.50"), "iface-lab")
        # Should match /16 (not deep enough for /24)
        self.assertEqual(self.trie.lookup_ip("10.1.2.50"), "iface-dept")
        # Should match /8 only
        self.assertEqual(self.trie.lookup_ip("10.99.99.99"), "iface-lan")

    def test_default_route(self):
        self.trie.insert_cidr("0.0.0.0/0", "default-gw")
        self.trie.insert_cidr("192.168.0.0/16", "iface-priv")
        self.assertEqual(self.trie.lookup_ip("8.8.8.8"), "default-gw")
        self.assertEqual(self.trie.lookup_ip("192.168.1.1"), "iface-priv")

    def test_no_match_returns_none(self):
        self.trie.insert_cidr("10.0.0.0/8", "iface-lan")
        self.assertIsNone(self.trie.lookup_ip("192.168.1.1"))

    def test_delete_prefix(self):
        self.trie.insert_cidr("10.0.0.0/8", "iface-lan")
        self.trie.insert_cidr("10.1.0.0/16", "iface-dept")
        ip = Packet.ip_to_int("10.1.0.0")
        self.assertTrue(self.trie.delete(ip, 16))
        # After deleting /16, should fall back to /8
        self.assertEqual(self.trie.lookup_ip("10.1.5.5"), "iface-lan")

    def test_delete_nonexistent_returns_false(self):
        ip = Packet.ip_to_int("10.0.0.0")
        self.assertFalse(self.trie.delete(ip, 8))

    def test_size_tracking(self):
        self.assertEqual(self.trie.size, 0)
        self.trie.insert_cidr("10.0.0.0/8", "a")
        self.trie.insert_cidr("172.16.0.0/12", "b")
        self.assertEqual(self.trie.size, 2)
        self.trie.delete(Packet.ip_to_int("10.0.0.0"), 8)
        self.assertEqual(self.trie.size, 1)

    def test_overlapping_prefixes_all_depths(self):
        self.trie.insert_cidr("10.0.0.0/8", "hop-8")
        self.trie.insert_cidr("10.1.0.0/16", "hop-16")
        self.trie.insert_cidr("10.1.1.0/24", "hop-24")
        self.trie.insert_cidr("10.1.1.128/25", "hop-25")
        self.assertEqual(self.trie.lookup_ip("10.1.1.200"), "hop-25")
        self.assertEqual(self.trie.lookup_ip("10.1.1.50"), "hop-24")

    def test_single_host_route(self):
        self.trie.insert_cidr("10.0.0.1/32", "host-route")
        self.trie.insert_cidr("10.0.0.0/24", "subnet")
        self.assertEqual(self.trie.lookup_ip("10.0.0.1"), "host-route")
        self.assertEqual(self.trie.lookup_ip("10.0.0.2"), "subnet")


if __name__ == "__main__":
    unittest.main()
