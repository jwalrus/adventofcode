from typing import Tuple, List

import pytest


def parse(x) -> Tuple[str, int]:
    return x[0], int(x[1:])


def up(start: complex, dist: int) -> List[complex]:
    return [start + complex(0, j) for j in range(1, dist + 1)]


def down(start: complex, dist: int) -> List[complex]:
    return [start - complex(0, j) for j in range(1, dist + 1)]


def right(start: complex, dist: int) -> List[complex]:
    return [start + complex(i, 0) for i in range(1, dist + 1)]


def left(start: complex, dist: int) -> List[complex]:
    return [start - complex(i, 0) for i in range(1, dist + 1)]


def line(start: complex, direction: Tuple[str, int]) -> List[complex]:
    match direction:
        case ("U", x):
            return up(start, x)
        case ("D", x):
            return down(start, x)
        case ("R", x):
            return right(start, x)
        case ("L", x):
            return left(start, x)


def path(start, directions) -> List[complex]:
    vertices = []
    for d in directions:
        vs = line(start, d)
        vertices = vertices + vs
        start = vs[-1]
    return vertices


def manhattan_distance(c: complex) -> int:
    return int(abs(c.real) + abs(c.imag))


def signal_delay(c: complex, one: List[complex], two: List[complex]) -> int:
    import itertools
    a = len(list(itertools.takewhile(lambda x: x != c, one))) + 1
    b = len(list(itertools.takewhile(lambda x: x != c, two))) + 1
    return a + b


def part1(puzzle):
    directions = [[parse(v) for v in wire] for wire in puzzle]
    one_vertices = set(path(0, directions[0]))
    two_vertices = set(path(0, directions[1]))
    return min([manhattan_distance(c) for c in one_vertices.intersection(two_vertices)])


def part2(puzzle):
    directions = [[parse(v) for v in wire] for wire in puzzle]
    one_vertices = path(0, directions[0])
    two_vertices = path(0, directions[1])
    intersection = set(one_vertices).intersection(two_vertices)
    return min([signal_delay(c, one_vertices, two_vertices) for c in intersection])


@pytest.fixture(scope="module")
def puzzle():
    with open("day03.txt") as f:
        lines = f.readlines()
        return [line.split(",") for line in lines]


class TestDay03:

    def test_puzzle_input(self, puzzle):
        assert len(puzzle) == 2

    def test_line(self):
        assert line(0, ("U", 2)) == [1j, 2j]
        assert line(0, ("D", 2)) == [-1j, -2j]
        assert line(0, ("R", 2)) == [1, 2]
        assert line(0, ("L", 2)) == [-1, -2]

    def test_path(self):
        directions = [("U", 2), ("R", 2)]
        assert path(0, directions) == [1j, 2j, 1 + 2j, 2 + 2j]

    @pytest.mark.parametrize('sample,distance', [
        ([["R75", "D30", "R83", "U83", "L12", "D49", "R71", "U7", "L72"],
          ["U62", "R66", "U55", "R34", "D71", "R55", "D58", "R83"]], 159),
        ([["R98", "U47", "R26", "D63", "R33", "U87", "L62", "D20", "R33", "U53", "R51"],
          ["U98", "R91", "D20", "R16", "D67", "R40", "U7", "R15", "U6", "R7"]], 135),
    ])
    def test_part1_samples(self, sample, distance):
        assert part1(sample) == distance

    def test_part1(self, puzzle):
        assert part1(puzzle) == 209

    @pytest.mark.parametrize('sample,distance', [
        ([["R75", "D30", "R83", "U83", "L12", "D49", "R71", "U7", "L72"],
          ["U62", "R66", "U55", "R34", "D71", "R55", "D58", "R83"]], 610),
        ([["R98", "U47", "R26", "D63", "R33", "U87", "L62", "D20", "R33", "U53", "R51"],
          ["U98", "R91", "D20", "R16", "D67", "R40", "U7", "R15", "U6", "R7"]], 410),
    ])
    def test_part2_samples(self, sample, distance):
        assert part2(sample) == distance

    def test_part2(self, puzzle):
        assert part2(puzzle) == 43258
