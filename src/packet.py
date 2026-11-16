from dataclasses import dataclass, field
import time


@dataclass
class Packet:
    src_ip: int
    dst_ip: int
    priority: int  # 0 (highest) to 7 (lowest)
    size: int  # bytes
    timestamp: float = field(default_factory=time.perf_counter)
    sequence: int = 0

    @staticmethod
    def ip_to_int(ip_str: str) -> int:
        octets = ip_str.split(".")
        return (int(octets[0]) << 24) | (int(octets[1]) << 16) | (int(octets[2]) << 8) | int(octets[3])

    @staticmethod
    def int_to_ip(ip_int: int) -> str:
        return f"{(ip_int >> 24) & 0xFF}.{(ip_int >> 16) & 0xFF}.{(ip_int >> 8) & 0xFF}.{ip_int & 0xFF}"


@dataclass
class RoutingEntry:
    prefix: int
    prefix_len: int
    next_hop: str

    @staticmethod
    def from_cidr(cidr: str, next_hop: str) -> "RoutingEntry":
        network, length = cidr.split("/")
        prefix_len = int(length)
        prefix = Packet.ip_to_int(network) >> (32 - prefix_len)
        return RoutingEntry(prefix=prefix, prefix_len=prefix_len, next_hop=next_hop)


@dataclass
class FlowRecord:
    src_ip: int
    dst_ip: int
    packet_count: int = 0
    byte_count: int = 0
    last_seen: float = 0.0

    @property
    def flow_key(self) -> tuple:
        return (self.src_ip, self.dst_ip)
