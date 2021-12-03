from collections import Counter
from typing import Dict, List

import pytest


def counts(bins: List[str]) -> Dict[int, Counter]:
    n = len(bins[0])
    return {i: Counter([b[i] for b in bins]) for i in range(n)}


def iter_to_str(xs):
    return ''.join([str(x) for x in xs])


def most_common(count) -> str:
    zeros, ones = count["0"], count["1"]
    return "0" if zeros > ones else "1"  # return "1" if tie


def least_common(count) -> str:
    return "0" if most_common(count) == "1" else "1"


def gamma(cs):
    return iter_to_str([most_common(c) for _, c in cs.items()])


def epsilon(gamma_):
    return iter_to_str(["0" if c == "1" else "1" for c in gamma_])


def bit_criteria(bins, position, *, criterion) -> str:
    if len(bins) == 1:
        return bins[0]
    cs = counts(bins)
    target = criterion(cs[position])
    bins = [b for b in bins if b[position] == target]
    return bit_criteria(bins, position + 1, criterion=criterion)


def oxygen_generator_rating(bins):
    return bit_criteria(bins, 0, criterion=most_common)


def co2_scrubber_rating(bins):
    return bit_criteria(bins, 0, criterion=least_common)


def part1(puzzle):
    g = gamma(counts(puzzle))
    e = epsilon(g)
    return int(g, 2) * int(e, 2)


def part2(puzzle):
    o = oxygen_generator_rating(puzzle)
    c = co2_scrubber_rating(puzzle)
    return int(o, 2) * int(c, 2)


class TestDay03:

    def test_puzzle_input(self, puzzle):
        assert len(puzzle) == 1000
        assert puzzle[:2] == ["111110110111", "100111000111"]

    def test_counts(self):
        bins = ["111", "110", "100", "001", "000"]
        assert counts(bins) == {
            0: Counter({"1": 3, "0": 2}),
            1: Counter({"1": 2, "0": 3}),
            2: Counter({"1": 2, "0": 3}),
        }

    def test_part1_sample(self, sample):
        assert part1(sample) == 198

    def test_gamma(self, sample):
        assert gamma(counts(sample)) == "10110"

    def test_epsilon(self, sample):
        assert epsilon("10110") == "01001"

    def test_part1(self, puzzle):
        assert part1(puzzle) == 3969000

    def test_oxygen_generator_rating(self, sample):
        assert oxygen_generator_rating(sample) == "10111"

    def test_co2_scrubber_rating(self, sample):
        assert co2_scrubber_rating(sample) == "01010"

    def test_part2_sample(self, sample):
        assert part2(sample) == 230

    def test_part2(self, puzzle):
        assert part2(puzzle) == 4267809


@pytest.fixture(scope="module")
def puzzle():
    with open("day03.txt") as f:
        return [b.strip() for b in f.readlines()]


@pytest.fixture(scope="module")
def sample():
    return [
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    ]
