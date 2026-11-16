"""Demo script showing the packet router in action."""

from src.router import Router
from src.packet import Packet


def main():
    router = Router()

    # Add routing entries
    routes = [
        ("0.0.0.0/0", "default-gw"),
        ("10.0.0.0/8", "iface-lan"),
        ("10.1.0.0/16", "iface-dept-a"),
        ("10.1.1.0/24", "iface-lab"),
        ("192.168.0.0/16", "iface-private"),
        ("172.16.0.0/12", "iface-vpn"),
    ]
    for cidr, hop in routes:
        router.add_route(cidr, hop)
    print(f"Loaded {router.route_count} routes\n")

    # Create sample packets with varying priorities
    packets = [
        Packet(Packet.ip_to_int("10.1.1.5"), Packet.ip_to_int("10.1.1.10"), priority=0, size=64),
        Packet(Packet.ip_to_int("10.1.2.1"), Packet.ip_to_int("192.168.1.1"), priority=3, size=512),
        Packet(Packet.ip_to_int("10.0.5.1"), Packet.ip_to_int("172.16.5.5"), priority=7, size=1500),
        Packet(Packet.ip_to_int("10.1.1.5"), Packet.ip_to_int("10.1.1.10"), priority=2, size=128),
        Packet(Packet.ip_to_int("8.8.8.8"), Packet.ip_to_int("1.1.1.1"), priority=5, size=256),
    ]

    # Process all packets
    print("--- Processing Packets ---")
    for pkt in packets:
        src = Packet.int_to_ip(pkt.src_ip)
        dst = Packet.int_to_ip(pkt.dst_ip)
        hop = router.process_packet(pkt)
        print(f"  {src} -> {dst}  priority={pkt.priority}  next_hop={hop}")

    print(f"\nActive flows: {router.active_flows}")
    print(f"Packets queued: {router.pending_packets}\n")

    # Forward packets in priority order
    print("--- Forwarding (priority order) ---")
    while router.pending_packets > 0:
        pkt, hop = router.forward_next()
        src = Packet.int_to_ip(pkt.src_ip)
        dst = Packet.int_to_ip(pkt.dst_ip)
        print(f"  [pri={pkt.priority}] {src} -> {dst}  via {hop}  ({pkt.size}B)")

    # Show flow stats
    print("\n--- Flow Stats ---")
    flow = router.get_flow_stats(
        Packet.ip_to_int("10.1.1.5"),
        Packet.ip_to_int("10.1.1.10"),
    )
    if flow:
        print(f"  10.1.1.5 -> 10.1.1.10: {flow.packet_count} packets, {flow.byte_count} bytes")


if __name__ == "__main__":
    main()
