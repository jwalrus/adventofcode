import itertools as it
import operator
from functools import reduce


def rotate_counterclockwise(grid):
    n_row, n_col = len(grid), len(grid[0])
    new_grid = [["."] * n_row for _ in range(n_col)]

    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            new_grid[n_col - j - 1][i] = grid[i][j]

    return new_grid


def rotate_clockwise(grid):
    return rotate_counterclockwise(rotate_counterclockwise(rotate_counterclockwise(grid)))


def score(grid):
    n = len(grid[0])
    result = 0
    for row in grid:
        for i, c in enumerate(row):
            if c == "O":
                result += n - i

    return result


def tilt(grid):
    new_grid = []
    for _, row in enumerate(grid):
        grouped_and_sorted = [sorted(list(g), reverse=True) for _, g in it.groupby(row, key=lambda x: x != "#")]
        new_row = reduce(operator.add, grouped_and_sorted)
        new_grid.append(new_row)

    return new_grid


def run_cycle(grid):
    north = tilt(grid)
    west = tilt(rotate_clockwise(north))
    south = tilt(rotate_clockwise(west))
    east = tilt(rotate_clockwise(south))
    return rotate_clockwise(east)


def part1(grid):
    return score(tilt(grid))


def part2(grid, n=1_000_000_000):
    def key(g):
        return "".join([c for line in g for c in line])

    cache = {}

    for cycle in range(1, n + 1):
        grid = run_cycle(grid)
        if key(grid) in cache:
            start_cycle = cache[key(grid)]
            break
        cache[key(grid)] = cycle

    delta = cycle - start_cycle
    new_start = (n - start_cycle) // delta * delta + start_cycle

    for cycle in range(new_start, n):
        grid = run_cycle(grid)

    return score(grid)


def main():
    with open(0) as f:
        grid = [[c for c in line] for line in f.read().splitlines()]
        grid = rotate_counterclockwise(grid)  # N is left hand side

    print("A:", part1(grid))  # 109,654
    print("B:", part2(grid))  # 94,876


if __name__ == "__main__":
    main()
