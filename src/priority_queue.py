class MinHeap:
    """Binary min-heap for QoS packet scheduling.

    Items are compared by (priority, sequence) so that higher-priority
    packets (lower number) are dequeued first, with FIFO order within
    the same priority level.
    """

    def __init__(self):
        self._heap: list = []
        self._seq = 0

    def __len__(self) -> int:
        return len(self._heap)

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def enqueue(self, item, priority: int) -> None:
        entry = (priority, self._seq, item)
        self._seq += 1
        self._heap.append(entry)
        self._sift_up(len(self._heap) - 1)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty heap")

        heap = self._heap
        root = heap[0]

        if len(heap) == 1:
            heap.pop()
        else:
            heap[0] = heap.pop()
            self._sift_down(0)

        return root[2]

    def peek(self):
        if self.is_empty():
            raise IndexError("peek at empty heap")
        return self._heap[0][2]

    def _sift_up(self, index: int) -> None:
        heap = self._heap
        while index > 0:
            parent = (index - 1) // 2
            if heap[index] < heap[parent]:
                heap[index], heap[parent] = heap[parent], heap[index]
                index = parent
            else:
                break

    def _sift_down(self, index: int) -> None:
        heap = self._heap
        size = len(heap)
        while True:
            smallest = index
            left = 2 * index + 1
            right = 2 * index + 2

            if left < size and heap[left] < heap[smallest]:
                smallest = left
            if right < size and heap[right] < heap[smallest]:
                smallest = right

            if smallest == index:
                break

            heap[index], heap[smallest] = heap[smallest], heap[index]
            index = smallest
