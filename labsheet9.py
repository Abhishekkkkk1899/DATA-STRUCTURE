
class Heap:
    def __init__(self, is_min=True):
        self.heap = []
        self.is_min = is_min

    def compare(self, a, b):
        return a < b if self.is_min else a > b

    def insert(self, value):
        self.heap.append(value)
        i = len(self.heap) - 1

        while i > 0:
            p = (i - 1) // 2
            if self.compare(self.heap[i], self.heap[p]):
                self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
                i = p
            else:
                break

    def extract(self):
        if not self.heap:
            return None

        root = self.heap[0]
        last = self.heap.pop()

        if self.heap:
            self.heap[0] = last
            i = 0

            while True:
                left = 2 * i + 1
                right = 2 * i + 2
                best = i

                if left < len(self.heap) and self.compare(
                        self.heap[left], self.heap[best]):
                    best = left
                if right < len(self.heap) and self.compare(
                        self.heap[right], self.heap[best]):
                    best = right

                if best == i:
                    break

                self.heap[i], self.heap[best] = self.heap[best], self.heap[i]
                i = best

        return root


data = [30, 10, 40, 5, 20]

for mode in [True, False]:
    h = Heap(mode)
    for x in data:
        h.insert(x)

    result = []
    while h.heap:
        result.append(h.extract())

    print("Min Heap:" if mode else "Max Heap:", result)
