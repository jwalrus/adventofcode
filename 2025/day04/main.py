def count(rolls, r, c):
    neighbors = {
        (r - 1, c), (r - 1, c + 1),
        (r, c + 1), (r + 1, c + 1),
        (r + 1, c), (r + 1, c - 1),
        (r, c - 1), (r - 1, c - 1),
    }

    return len(rolls & neighbors)


def rolls_of_paper(grid):
    return {
        (r, c)
        for r, row in enumerate(grid)
        for c, val in enumerate(row)
        if val == "@"
    }


def run(rolls):
    removed = set()
    for r, c in rolls:
        if count(rolls, r, c) < 4:
            removed.add((r, c))

    return removed


def part1(grid):
    return len(run(rolls_of_paper(grid)))


def part2(grid):
    rolls = rolls_of_paper(grid)

    result = 0
    while removed := run(rolls):
        result += len(removed)
        rolls = rolls - removed

    return result


if __name__ == "__main__":
    import sys

    with open(sys.argv[1], "r") as fh:
        data = [list(line.strip()) for line in fh.readlines()]

    print("part1", part1(data))
    print("part2", part2(data))
