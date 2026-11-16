class HashNode:
    __slots__ = ("key", "value", "next")

    def __init__(self, key, value, next_node=None):
        self.key = key
        self.value = value
        self.next = next_node


class ChainingHashTable:
    """Hash table with separate chaining for collision resolution."""

    INITIAL_CAPACITY = 16
    LOAD_FACTOR_THRESHOLD = 0.75

    def __init__(self, capacity: int = INITIAL_CAPACITY):
        self.capacity = capacity
        self.buckets: list[HashNode | None] = [None] * capacity
        self.size = 0

    def _hash(self, key) -> int:
        h = hash(key)
        # Spread bits to reduce clustering
        h ^= (h >> 16)
        return h % self.capacity

    def insert(self, key, value) -> None:
        index = self._hash(key)
        node = self.buckets[index]

        while node is not None:
            if node.key == key:
                node.value = value
                return
            node = node.next

        new_node = HashNode(key, value, self.buckets[index])
        self.buckets[index] = new_node
        self.size += 1

        if self.size / self.capacity > self.LOAD_FACTOR_THRESHOLD:
            self._resize()

    def lookup(self, key):
        index = self._hash(key)
        node = self.buckets[index]

        while node is not None:
            if node.key == key:
                return node.value
            node = node.next

        return None

    def delete(self, key) -> bool:
        index = self._hash(key)
        node = self.buckets[index]
        prev = None

        while node is not None:
            if node.key == key:
                if prev is None:
                    self.buckets[index] = node.next
                else:
                    prev.next = node.next
                self.size -= 1
                return True
            prev = node
            node = node.next

        return False

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0

        for node in old_buckets:
            while node is not None:
                self.insert(node.key, node.value)
                node = node.next

    @property
    def load_factor(self) -> float:
        return self.size / self.capacity

    def keys(self):
        for node in self.buckets:
            while node is not None:
                yield node.key
                node = node.next
