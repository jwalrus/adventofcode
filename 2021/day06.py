from collections import Counter
from typing import Dict

import more_itertools as mit
import pytest


def advance(cnt: Dict[int, int]) -> Dict[int, int]:
    d = {}
    for i in range(9):
        match i:
            case 6:
                d[6] = cnt.get(0, 0) + cnt.get(7, 0)
            case 8:
                d[8] = cnt.get(0, 0)
            case _:
                d[i] = cnt.get(i + 1, 0)
    return d


def generate_days(d):
    while True:
        yield (d := advance(d))


def part1(puzzle, n=80):
    days = generate_days(Counter(puzzle))
    return sum([v for _, v in mit.last(mit.take(n, days)).items()])


def part2(puzzle):
    return part1(puzzle, n=256)


class TestDay06:

    def test_puzzle_input(self, puzzle):
        assert puzzle[-1] == 2

    def test_advance(self):
        cnt = {0: 3, 7: 4, 3: 2}
        assert dict(advance(cnt)) == {0: 0, 1: 0, 2: 2, 3: 0, 4: 0, 5: 0, 6: 7, 7: 0, 8: 3}

    def test_part1_sample(self, sample):
        assert part1(sample) == 5934

    def test_part1(self, puzzle):
        assert part1(puzzle) == 380243

    def test_part2_sample(self, sample):
        assert part2(sample) == 26984457539

    def test_part2(self, puzzle):
        assert part2(puzzle) == 1708791884591


def parse_input(text):
    return [int(x) for x in text.strip().split(',')]


@pytest.fixture(scope="module")
def puzzle():
    with open("day06.txt") as f:
        return parse_input(f.read())


@pytest.fixture(scope="module")
def sample():
    s = """3,4,3,1,2"""
    return parse_input(s)
