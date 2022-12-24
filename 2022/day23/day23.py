import sys

from collections import Counter

N = [(-1, -1), (0, -1), (1, -1)]
S = [(-1, 1), (0, 1), (1, 1)]
W = [(-1, 1), (-1, 0), (-1, -1)]
E = [(1, 1), (1, 0), (1, -1)]


def gen_directions():
    base = [N, S, W, E]
    while True:
        yield base
        base = base[1:] + [base[0]]


def proposal(elf, elves, directions):
    x, y = elf
    if all((x + dx, y + dy) not in elves for d in directions for dx, dy in d):
        return elf

    for d in directions:
        if all((x + dx, y + dy) not in elves for dx, dy in d):
            return x + d[1][0], y + d[1][1]

    return elf


def bounds(elves):
    min_x = min(x for x, _ in elves)
    max_x = max(x for x, _ in elves)
    min_y = min(y for _, y in elves)
    max_y = max(y for _, y in elves)
    return min_x, max_x, min_y, max_y


def run(elves, n):
    for i, directions in enumerate(gen_directions()):
        cp = set(elves)
        proposals = {elf: proposal(elf, cp, directions) for elf in elves}
        counts = Counter(p for _, p in proposals.items())
        elves = [proposals[e] if counts[proposals[e]] == 1 else e for e in elves]

        if all(e == p for e, p in proposals.items()) or (i + 1) == n:
            min_x, max_x, min_y, max_y = bounds(elves)
            return i + 1, sum(
                1
                for y in range(min_y, max_y + 1)
                for x in range(min_x, max_x + 1)
                if (x, y) not in elves
            )

    return 0


def main():
    with open(sys.argv[1], "r") as f:
        lines = f.read().split("\n")
        elves = [
            (c, r)  # (x, y)
            for r, row in enumerate(lines)
            for c, col in enumerate(row)
            if col == "#"
        ]

    print("part1:", run(elves, 10))  # 3940
    print("part1:", run(elves, -1))  # 990


if __name__ == "__main__":
    main()
