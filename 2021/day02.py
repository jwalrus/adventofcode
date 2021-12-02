from itertools import accumulate, islice
from typing import Tuple

from more_itertools import last
import pytest

Step = Tuple[str, int]
Coord = complex
Aim = int
Position = Tuple[Coord, Aim]


def move(start: Coord, step: Step) -> Coord:
    match step:
        case ("forward", x):
            return start + Coord(x, 0)
        case ("down", y):
            return start + Coord(0, y)
        case ("up", y):
            return start - Coord(0, y)


def aim(start: Position, step: Step) -> Position:
    pos, aim = start
    match step:
        case ("forward", x):
            return pos + Coord(x, x * aim), aim
        case ("down", y):
            return pos, aim + y
        case ("up", y):
            return pos, aim - y


def path(start, steps, advance=move):
    return islice(accumulate(steps, func=advance, initial=start), 1, None)


def part1(puzzle) -> int:
    stop = last(path(0, puzzle))
    return int(stop.real * stop.imag)


def part2(puzzle) -> int:
    stop = last(path((0j, 0), puzzle, advance=aim))
    coord, _ = stop
    return int(coord.real * coord.imag)


@pytest.fixture(scope="module")
def puzzle():
    with open("day02.txt") as f:
        data = f.readlines()
        xs = [x.split(" ") for x in data]
        return [(x[0], int(x[1])) for x in xs]


class TestDay02:

    def test_puzzle_input(self, puzzle):
        assert len(puzzle) == 1000
        assert puzzle[0] == ("forward", 8)

    def test_path(self, puzzle):
        steps = [("forward", 8), ("down", 10), ("up", 5)]
        assert list(path(0, steps)) == [8, 8 + 10j, 8 + 5j]

    def test_part1_sample(self):
        sample = [("forward", 5), ("down", 5), ("forward", 8), ("up", 3), ("down", 8), ("forward", 2)]
        assert part1(sample) == 150

    def test_part1(self, puzzle):
        assert part1(puzzle) == 1654760

    def test_path_with_aim(self):
        steps = [("down", 10), ("forward", 8), ("up", 5)]
        actual = list(path((0j, 0), steps, advance=aim))
        expected = [(Coord(0, 0), Aim(10)), (Coord(8, 80), Aim(10)), (Coord(8, 80), Aim(5))]
        assert actual == expected

    def test_part2_sample(self):
        sample = [("forward", 5), ("down", 5), ("forward", 8), ("up", 3), ("down", 8), ("forward", 2)]
        assert part2(sample) == 900

    def test_part2(self, puzzle):
        assert part2(puzzle) == 1956047400
