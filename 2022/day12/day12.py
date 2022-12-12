import sys
from collections import deque


def find(target, hmap):
    return [
        (i, j)
        for i, h in enumerate(hmap)
        for j, w in enumerate(h)
        if w == target
    ]


def height(x):
    match x:
        case 'S':
            return ord('a')
        case 'E':
            return ord('z')
        case _:
            return ord(x)


class Neighbors:
    def __init__(self, hmap):
        self.h = len(hmap)
        self.w = len(hmap[0])

    def __call__(self, col, row):
        return [
            (col + dh, row + dw)
            for dh, dw in [(1, 0), (-1, 0), (0, -1), (0, 1)]
            if 0 <= row + dw < self.w and 0 <= col + dh < self.h and (dh, dw) != (0, 0)
        ]


def part1(hmap, start):
    neighbors = Neighbors(hmap)
    queue = deque()
    queue.append((start, 0))
    visited = {start}

    while queue:
        (h, w), depth = queue.popleft()

        if hmap[h][w] == 'E':
            return depth

        _next = [
            (n, depth + 1)
            for n in neighbors(h, w)
            if height(hmap[n[0]][n[1]]) - height(hmap[h][w]) <= 1 and n not in visited
        ]

        for n in _next:
            queue.append(n)
            visited.add(n[0])

    return 9999999999999999


def part2(hmap):
    starts = find('a', hmap) + find('S', hmap)
    dists = [part1(hmap, start) for start in starts]
    return min(dists)


def main():
    with open(sys.argv[1], "r") as f:
        lines = f.read().split("\n")
        print("== Day 12, 2022 ==")
        print("part1:", part1(lines, find('S', lines)[0]))  # 517
        print("part2:", part2(lines))  # 512


if __name__ == '__main__':
    main()
