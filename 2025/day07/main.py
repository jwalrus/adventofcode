from functools import cache


def find_s(g):
    for r, row in enumerate(g):
        for c, val in enumerate(row):
            if val == "S":
                return r, c
    return None


def part1(g):
    n_row, n_col = len(g), len(g[0])
    splits = set()

    @cache
    def recur(r, c):
        if g[r][c] != "^":
            if r + 1 < n_row:
                recur(r + 1, c)
            return

        splits.add((r, c))
        if 0 <= c - 1:
            recur(r, c - 1)

        if c + 1 < n_col:
            recur(r, c + 1)

    recur(*find_s(g))
    return len(splits)


def part2(g):
    n_row, n_col = len(g), len(g[0])

    @cache
    def recur(r, c):
        if g[r][c] != "^":
            if r + 1 < n_row:
                return recur(r + 1, c)
            return 1

        left, right = 0, 0

        if 0 <= c - 1:
            left = recur(r, c - 1)

        if c + 1 < n_col:
            right = recur(r, c + 1)

        return left + right

    return recur(*find_s(g))


if __name__ == "__main__":
    import sys

    with open(sys.argv[1], "r") as fh:
        grid = fh.read().splitlines()

    print("part1", part1(grid))
    print("part2", part2(grid))
