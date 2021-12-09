import itertools as it
from functools import reduce
from operator import mul
from typing import Dict, List, Tuple

import pytest

Coord = Tuple[int, int]
HeightMap = Dict[Coord, int]


def neighbors(c: Coord) -> List[Coord]:
    x, y = c
    return [(x, y - 1), (x + 1, y), (x - 1, y), (x, y + 1)]


def is_low_point(c: Coord, hmap: HeightMap) -> bool:
    return all(hmap[c] < hmap.get(n) for n in neighbors(c) if hmap.get(n) is not None)


def find_low_points(hmap: HeightMap) -> List[Coord]:
    return [c for c in hmap if is_low_point(c, hmap)]


def basin(start: Coord, hmap: HeightMap) -> List[Coord]:
    def higher_neighbors(c):
        return [n for n in neighbors(c)
                if hmap.get(n) is not None
                and hmap.get(n) != 9
                and hmap.get(n) > hmap.get(c)]

    ns = higher_neighbors(start)
    if not ns:
        return [start]
    else:
        return [start] + list(it.chain.from_iterable(basin(n, hmap) for n in ns))


def part1(puzzle):
    return sum(puzzle[c] + 1 for c in find_low_points(puzzle))


def part2(puzzle):
    basins = [len(set(basin(c, puzzle))) for c in find_low_points(puzzle)]
    return reduce(mul, sorted(basins)[-3:])


class TestDay09:

    def test_puzzle_input(self, sample, puzzle):
        assert len(sample) == 50
        assert len(puzzle) == 100 * 100

    def test_neighbors(self, sample):
        assert neighbors((0, 0)) == [(0, -1), (1, 0), (-1, 0), (0, 1)]

    def test_is_low_point(self, sample):
        assert is_low_point((0, 1), sample)
        assert not is_low_point((3, 3), sample)

    def test_basin(self, sample):
        assert basin((0, 1), sample) == [(0, 1), (0, 0), (1, 0)]
        assert len(set(basin((2, 2), sample))) == 14

    def test_part1_sample(self, sample):
        assert part1(sample) == 15

    def test_part1(self, puzzle):
        assert part1(puzzle) == 436

    def test_part2_sample(self, sample):
        assert part2(sample) == 1134

    def test_part2(self, puzzle):
        assert part2(puzzle) == 1317792


def parse_input(text):
    lines = [x.strip() for x in text.split("\n") if x != ""]
    xs = [[int(x) for x in list(line)] for line in lines]
    return {(i, j): x for i, row in enumerate(xs) for j, x in enumerate(row)}


@pytest.fixture(scope="module")
def puzzle():
    with open("day09.txt") as f:
        return parse_input(f.read())


@pytest.fixture(scope="module")
def sample():
    s = """2199943210
3987894921
9856789892
8767896789
9899965678
"""
    return parse_input(s)
