import sys
from collections import defaultdict
from itertools import pairwise


def main():
    with open(sys.argv[1]) as f:
        nums = [int(i) for i in f.read().splitlines()]
        print("part1:", part1(nums))
        print("part2:", part2(nums))


def part1(nums):
    result = 0
    for n in nums:
        xs = [n] + [n := nxt(n) for _ in range(2000)]
        result += xs[-1]
    return result


def part2(nums):
    result = defaultdict(int)
    for n in nums:
        xs = [n] + [n := nxt(n) for _ in range(2000)]
        prices = [x % 10 for x in xs]
        diffs = [b % 10 - a % 10 for a, b in pairwise(prices)]

        temp = dict()
        for i in range(len(xs) - 4):
            seq = tuple(diffs[i:i + 4])
            if seq not in temp:
                temp[seq] = prices[i + 4]

        for k, v in temp.items():
            result[k] += v

    return max(result.values())


def nxt(n):
    n = prune(mix(n, n * 64))
    n = prune(mix(n, n // 32))
    n = prune(mix(n, n * 2048))
    return n


def mix(n, a):
    return n ^ a


def prune(n):
    return n % 16777216


if __name__ == '__main__':
    main()
