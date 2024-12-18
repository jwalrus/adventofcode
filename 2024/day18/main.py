import sys
from collections import deque


def main():
    with open(sys.argv[1]) as fh:
        cbytes = [line.split(",") for line in fh.read().splitlines()]
        cbytes = [(int(a), int(b)) for a, b in cbytes]
        # # sample
        # print("part1:", len(part1(cbytes, 12, 6))-1)
        # print("part2:", part2(cbytes, 12, 6))

        # puzzle
        print("part1:", len(part1(cbytes, 1024, 70)) - 1)
        print("part2:", part2(cbytes, 1024, 70))


def part1(cbytes, n, size):
    mem_space = [["." for _ in range(size + 1)] for _ in range(size + 1)]
    for c, r in cbytes[:n]:
        mem_space[r][c] = "#"
    cur = (0, 0)
    queue = deque()
    queue.append((cur, [cur]))
    visited = set()

    while queue:
        cur, path = queue.popleft()
        if cur in visited:
            continue
        visited.add(cur)
        r, c = cur

        if c < 0 or r < 0 or c > size or r > size or mem_space[r][c] == "#":
            continue

        if cur == (size, size):
            return path

        for (dc, dr) in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
            p = (r + dr, c + dc)

            queue.append((p, path + [p]))

    return []


def part2(cbytes, n, size):
        lo, hi = n - 1, len(cbytes)
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if part1(cbytes, mid, size):
                lo = mid
            else:
                hi = mid
        return cbytes[mid]


if __name__ == '__main__':
    main()
