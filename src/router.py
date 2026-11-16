import time
from .trie import BinaryTrie
from .hash_table import ChainingHashTable
from .priority_queue import MinHeap
from .packet import Packet, FlowRecord


class Router:
    """Simulated packet router integrating trie, hash table, and priority queue."""

    def __init__(self):
        self.routing_table = BinaryTrie()
        self.flow_table = ChainingHashTable()
        self.scheduler = MinHeap()
        self._seq = 0

    def add_route(self, cidr: str, next_hop: str) -> None:
        self.routing_table.insert_cidr(cidr, next_hop)

    def process_packet(self, packet: Packet) -> str | None:
        next_hop = self.routing_table.lookup(packet.dst_ip)
        if next_hop is None:
            return None

        flow_key = (packet.src_ip, packet.dst_ip)
        record = self.flow_table.lookup(flow_key)
        if record is None:
            record = FlowRecord(src_ip=packet.src_ip, dst_ip=packet.dst_ip)
            self.flow_table.insert(flow_key, record)
        record.packet_count += 1
        record.byte_count += packet.size
        record.last_seen = time.perf_counter()

        packet.sequence = self._seq
        self._seq += 1
        self.scheduler.enqueue(packet, packet.priority)

        return next_hop

    def forward_next(self) -> tuple[Packet, str] | None:
        if self.scheduler.is_empty():
            return None

        packet = self.scheduler.dequeue()
        next_hop = self.routing_table.lookup(packet.dst_ip)
        return (packet, next_hop)

    def get_flow_stats(self, src_ip: int, dst_ip: int) -> FlowRecord | None:
        return self.flow_table.lookup((src_ip, dst_ip))

    @property
    def pending_packets(self) -> int:
        return len(self.scheduler)

    @property
    def active_flows(self) -> int:
        return self.flow_table.size

    @property
    def route_count(self) -> int:
        return self.routing_table.size
