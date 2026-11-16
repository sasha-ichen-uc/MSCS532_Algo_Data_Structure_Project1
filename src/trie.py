class TrieNode:
    __slots__ = ("children", "next_hop")

    def __init__(self):
        self.children: list = [None, None]
        self.next_hop: str | None = None


class BinaryTrie:
    """Binary trie for longest-prefix matching on IPv4 addresses."""

    def __init__(self):
        self.root = TrieNode()
        self.size = 0

    def insert(self, ip: int, prefix_len: int, next_hop: str) -> None:
        node = self.root
        for i in range(prefix_len):
            bit = (ip >> (31 - i)) & 1
            if node.children[bit] is None:
                node.children[bit] = TrieNode()
            node = node.children[bit]
        node.next_hop = next_hop
        self.size += 1

    def lookup(self, ip: int) -> str | None:
        node = self.root
        best_match = node.next_hop
        for i in range(32):
            bit = (ip >> (31 - i)) & 1
            if node.children[bit] is None:
                break
            node = node.children[bit]
            if node.next_hop is not None:
                best_match = node.next_hop
        return best_match

    def delete(self, ip: int, prefix_len: int) -> bool:
        path = [self.root]
        node = self.root
        for i in range(prefix_len):
            bit = (ip >> (31 - i)) & 1
            if node.children[bit] is None:
                return False
            node = node.children[bit]
            path.append(node)

        if path[-1].next_hop is None:
            return False

        path[-1].next_hop = None
        self.size -= 1

        for i in range(len(path) - 1, 0, -1):
            node = path[i]
            if node.next_hop is not None or node.children[0] is not None or node.children[1] is not None:
                break
            bit = (ip >> (31 - (i - 1))) & 1
            path[i - 1].children[bit] = None

        return True

    def insert_cidr(self, cidr: str, next_hop: str) -> None:
        network, length = cidr.split("/")
        prefix_len = int(length)
        ip = self._ip_to_int(network)
        self.insert(ip, prefix_len, next_hop)

    def lookup_ip(self, ip_str: str) -> str | None:
        return self.lookup(self._ip_to_int(ip_str))

    @staticmethod
    def _ip_to_int(ip_str: str) -> int:
        octets = ip_str.split(".")
        return (int(octets[0]) << 24) | (int(octets[1]) << 16) | (int(octets[2]) << 8) | int(octets[3])
