import itertools as it
from collections import Counter
from typing import Tuple, Iterable

import pytest

Coord = complex
Path = Tuple[Coord, Coord]


def line(path: Path, include_diag=False) -> Iterable[Coord]:
    def ud(x, y):
        """up and down"""
        mn, mx = (x, y) if x <= y else (y, x)
        return range(int(mn), int(mx) + 1)

    def dg(one: Coord, two: Coord):
        """diagonal"""
        x1, y1, x2, y2 = int(one.real), int(one.imag), int(two.real), int(two.imag)
        x_dir = 1 if x2 > x1 else -1
        y_dir = 1 if y2 > y1 else -1
        return zip(range(x1, x2 + x_dir, x_dir), range(y1, y2 + y_dir, y_dir))

    match path:
        case (l, r) if l.real == r.real:
            return (Coord(r.real, i) for i in ud(l.imag, r.imag))
        case (l, r) if l.imag == r.imag:
            return (Coord(i, r.imag) for i in ud(l.real, r.real))
        case (l, r) if include_diag:
            return (Coord(i, j) for i, j in dg(l, r))
        case _:
            return []


def part1(puzzle, include_diag=False):
    all_coords = it.chain.from_iterable(line(c, include_diag=include_diag) for c in puzzle)
    counter = Counter(all_coords)
    return len([k for k, v in counter.items() if v > 1])


def part2(puzzle):
    return part1(puzzle, include_diag=True)


class TestDay03:

    def test_puzzle_input(self, puzzle):
        assert len(puzzle) == 500
        assert puzzle[0] == (818 + 513j, 818 + 849j)

    def test_lines(self):
        assert list(line((0, 0 + 3j))) == [0, 1j, 2j, 3j]
        assert list(line((0 + 1j, 3 + 1j))) == [0 + 1j, 1 + 1j, 2 + 1j, 3 + 1j]
        assert list(line((0 + 2j, 2 + 0j), include_diag=True)) == [0 + 2j, 1 + 1j, 2 + 0j]
        assert list(line((0 + 0j, 2 + 2j), include_diag=True)) == [0 + 0j, 1 + 1j, 2 + 2j]

    def test_part1_sample(self, sample):
        assert part1(sample) == 5

    def test_part1(self, puzzle):
        assert part1(puzzle) == 6007

    def test_part2_sample(self, sample):
        assert part2(sample) == 12

    def test_part2(self, puzzle):
        assert part2(puzzle) == 19349


def parse_input(text):
    def to_coord(x):
        r, i = x.strip().split(",")
        return complex(int(r), int(i))

    lines = (line.split(" -> ") for line in text.strip().split("\n"))
    return [(to_coord(x), to_coord(y)) for x, y in lines]


@pytest.fixture(scope="module")
def puzzle():
    with open("day05.txt") as f:
        return parse_input(f.read())


@pytest.fixture(scope="module")
def sample():
    s = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""
    return parse_input(s)
