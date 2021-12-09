import itertools as it
from typing import Iterable
import itertools as it

import more_itertools as mit
import pytest


def part1(puzzle):
    return -1


def part2(puzzle):
    return -1


class TestDay09:

    def test_puzzle_input(self, sample, puzzle):
        assert len(sample) == 10
        assert len(puzzle) == 200

    def test_part1_sample(self, sample):
        assert part1(sample) == 0

    def test_part1(self, puzzle):
        assert part1(puzzle) == 0

    def test_part2_sample(self, sample):
        assert part2(sample) == 0

    def test_part2(self, puzzle):
        assert part2(puzzle) == 0


def parse_input(text):
    lines = [line.strip() for line in text.split("\n")]
    in_out = [tuple(line.split(" | ")) for line in lines]
    return [(i.split(" "), o.split(" ")) for i, o in in_out]


@pytest.fixture(scope="module")
def puzzle():
    with open("day09.txt") as f:
        return parse_input(f.read())


@pytest.fixture(scope="module")
def sample():
    s = """
    """
    return parse_input(s)
