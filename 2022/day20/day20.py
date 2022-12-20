import sys

from collections import deque


def mix(orig, nums):
    d = deque(nums)
    n = len(nums)

    for x in orig:
        ix = d.index(x)
        nx = (ix + x[1]) % (n - 1) if (ix + x[1] != 0) else (n - 1)
        d.remove(x)
        d.insert(nx, x)

    return d


def coordinates(d):
    xs = deque([x for _, x in d])
    iz = xs.index(0)
    xs.rotate(-iz)
    n = len(xs)
    return xs[1000 % n] + xs[2000 % n] + xs[3000 % n]


def part1(nums, n):
    d = deque(nums)
    for _ in range(n):
        d = mix(nums, d)
    return coordinates(d)


def main():
    with open(sys.argv[1], "r") as f:
        nums = [(i, int(x)) for i, x in enumerate(f.read().split("\n"))]
        nums2 = [(i, x * 811589153) for i, x in nums]

    print("part1:", part1(nums, 1))  # 4267
    print("part2:", part1(nums2, 10))  # 6871725358451


if __name__ == '__main__':
    main()
