"""Tests for the integrated Router class."""

import unittest
from src.router import Router
from src.packet import Packet


class TestRouter(unittest.TestCase):

    def setUp(self):
        self.router = Router()
        self.router.add_route("0.0.0.0/0", "default-gw")
        self.router.add_route("10.0.0.0/8", "iface-lan")
        self.router.add_route("10.1.1.0/24", "iface-lab")

    def _make_packet(self, src="10.0.0.1", dst="10.1.1.5", pri=0, size=64):
        return Packet(Packet.ip_to_int(src), Packet.ip_to_int(dst), pri, size)

    def test_process_packet_returns_next_hop(self):
        pkt = self._make_packet(dst="10.1.1.5")
        hop = self.router.process_packet(pkt)
        self.assertEqual(hop, "iface-lab")

    def test_process_packet_default_route(self):
        pkt = self._make_packet(dst="8.8.8.8")
        hop = self.router.process_packet(pkt)
        self.assertEqual(hop, "default-gw")

    def test_flow_tracking(self):
        for _ in range(5):
            pkt = self._make_packet(src="10.0.0.1", dst="10.1.1.5", size=100)
            self.router.process_packet(pkt)
        flow = self.router.get_flow_stats(
            Packet.ip_to_int("10.0.0.1"),
            Packet.ip_to_int("10.1.1.5"),
        )
        self.assertEqual(flow.packet_count, 5)
        self.assertEqual(flow.byte_count, 500)

    def test_scheduling_priority_order(self):
        pkts = [
            self._make_packet(pri=7, dst="10.1.1.1"),
            self._make_packet(pri=0, dst="10.1.1.2"),
            self._make_packet(pri=3, dst="10.1.1.3"),
        ]
        for p in pkts:
            self.router.process_packet(p)

        fwd1 = self.router.forward_next()
        fwd2 = self.router.forward_next()
        fwd3 = self.router.forward_next()
        self.assertEqual(fwd1[0].priority, 0)
        self.assertEqual(fwd2[0].priority, 3)
        self.assertEqual(fwd3[0].priority, 7)

    def test_forward_empty_returns_none(self):
        self.assertIsNone(self.router.forward_next())

    def test_active_flows_count(self):
        self.assertEqual(self.router.active_flows, 0)
        self.router.process_packet(self._make_packet(src="1.1.1.1", dst="2.2.2.2"))
        self.router.process_packet(self._make_packet(src="3.3.3.3", dst="4.4.4.4"))
        self.assertEqual(self.router.active_flows, 2)

    def test_pending_packets_count(self):
        self.router.process_packet(self._make_packet())
        self.router.process_packet(self._make_packet())
        self.assertEqual(self.router.pending_packets, 2)
        self.router.forward_next()
        self.assertEqual(self.router.pending_packets, 1)

    def test_end_to_end_pipeline(self):
        # Process, schedule, forward, check stats
        pkt = self._make_packet(src="10.0.0.1", dst="10.1.1.99", pri=2, size=256)
        hop = self.router.process_packet(pkt)
        self.assertEqual(hop, "iface-lab")
        self.assertEqual(self.router.pending_packets, 1)

        fwd_pkt, fwd_hop = self.router.forward_next()
        self.assertEqual(fwd_pkt.priority, 2)
        self.assertEqual(fwd_pkt.size, 256)
        self.assertEqual(fwd_hop, "iface-lab")
        self.assertEqual(self.router.pending_packets, 0)


if __name__ == "__main__":
    unittest.main()
