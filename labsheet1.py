
import time

def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

sizes = [10000, 50000, 100000]

for n in sizes:
    arr = list(range(1, n + 1))
    target = n

    start = time.perf_counter()
    result = linear_search(arr, target)
    end = time.perf_counter()

    print("Array Size:", n)
    print("Position:", result + 1)
    print("Execution Time:", round((end - start) * 1_000_000, 2), "microseconds")
    print()
