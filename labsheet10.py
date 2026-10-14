
def solve(N, nums):
    count = 0

    for i in range(N):
        for j in range(i + 1, N):
            sum1 = sum(map(int, str(nums[i])))
            sum2 = sum(map(int, str(nums[j])))

            if sum1 == sum2:
                count += 1

    return count


N = int(input())
nums = list(map(int, input().split()))

print(solve(N, nums))
