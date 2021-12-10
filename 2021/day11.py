import itertools as it
from collections import Counter
from typing import List, Tuple, Dict, Set

import more_itertools as mit
import pytest

Point = Tuple[int, int]
Grid = Dict[Point, int]


def make_grid(grid: List[List[int]]) -> Grid:
    return {(i, j): x for i, row in enumerate(grid) for j, x in enumerate(row)}


def neighbors(p: Point, grid: Grid) -> List[Point]:
    x, y = p
    ns = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y),
          (x + 1, y + 1), (x + 1, y - 1), (x - 1, y - 1), (x - 1, y + 1)]
    return [n for n in ns if grid.get(n) is not None]


def go(grid: Grid, flashed: Set[Point] = frozenset()):
    new_flashes = {p for p, v in grid.items() if v > 9 and p not in flashed}
    if not new_flashes:
        return grid, flashed
    else:
        flashed = flashed.union(new_flashes)
        updates = Counter(n for p in new_flashes for n in neighbors(p, grid) if n not in flashed)
        new_grid = {p: v + updates.get(p, 0) for p, v in grid.items()}
        return go(new_grid, flashed)


def step(grid: Grid, flashes: int = 0):
    new_grid, flashed = go({p: v + 1 for p, v in grid.items()})
    return {p: 0 if v > 9 else v for p, v in new_grid.items()}, flashes + len(flashed)


def steps(grid, iterable):
    return it.accumulate(
        iterable,
        func=lambda acc, _: step(acc[0], acc[1]),
        initial=(grid, 0)
    )


def part1(puzzle, n=100):
    return mit.last(steps(make_grid(puzzle), range(n)))[1]


def part2(puzzle):
    xs = steps(make_grid(puzzle), it.count())
    return mit.ilen(it.takewhile(lambda acc: any(v != 0 for v in acc[0].values()), xs))


class TestDay11:

    def test_puzzle_input(self, sample, puzzle):
        assert len(sample) == 10
        assert len(puzzle) == 10
        assert len(puzzle[0]) == 10

    def test_part1_sample(self, sample):
        assert part1(sample) == 1656

    def test_part1(self, puzzle):
        assert part1(puzzle) == 1615

    def test_part2_sample(self, sample):
        assert part2(sample) == 195

    def test_part2(self, puzzle):
        assert part2(puzzle) == 249


def parse_input(text):
    return [[int(x) for x in list(line.strip())] for line in text.split("\n") if line != ""]


@pytest.fixture(scope="module")
def puzzle():
    return parse_input("""4738615556
6744423741
2812868827
8844365624
4546674266
4518674278
7457237431
4524873247
3153341314
3721414667
""")


@pytest.fixture(scope="module")
def sample():
    s = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""
    return parse_input(s)


@pytest.fixture
def little_sample():
    return parse_input("""11111
19991
19191
19991
11111
""")
