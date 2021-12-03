import numpy as np
import pytest


def to_array(bins):
    return np.array([[int(x) for x in list(b)] for b in bins])


def find_most_common(arr):
    return arr.mean(axis=0)  # column-wise


def arr_to_str(arr):
    return ''.join([str(x) for x in arr])


def gamma(bins):
    return arr_to_str(np.where(find_most_common(bins) > 0.5, 1, 0))


def epsilon(gamma_):
    return ''.join(["0" if c == "1" else "1" for c in gamma_])


def oxygen_generator_rating(bins, position):
    if len(bins) == 1:
        return arr_to_str(bins[0])
    most_common = find_most_common(bins)
    target = 1 if most_common[position] == 0.5 else (1 if most_common[position] > 0.5 else 0)
    mask = bins[:, position] == target
    return oxygen_generator_rating(bins[mask], position + 1)


def co2_scrubber_rating(bins, position):
    if len(bins) == 1:
        return arr_to_str(bins[0])
    most_common = find_most_common(bins)
    target = 0 if most_common[position] == 0.5 else (0 if most_common[position] > 0.5 else 1)
    mask = bins[:, position] == target
    return co2_scrubber_rating(bins[mask], position + 1)


def part1(puzzle):
    arr = to_array(puzzle)
    g = gamma(arr)
    e = epsilon(g)
    return int(g, 2) * int(e, 2)


def part2(puzzle):
    arr = to_array(puzzle)
    o = oxygen_generator_rating(arr, 0)
    c = co2_scrubber_rating(arr, 0)
    return int(o, 2) * int(c, 2)


class TestDay03:

    def test_puzzle_input(self, puzzle):
        assert len(puzzle) == 1000
        assert puzzle[:2] == ["111110110111", "100111000111"]

    def test_part1_sample(self, sample):
        assert part1(sample) == 198

    def test_gamma(self, sample):
        assert gamma(to_array(sample)) == "10110"

    def test_epsilon(self, sample):
        assert epsilon("10110") == "01001"

    def test_part1(self, puzzle):
        assert part1(puzzle) == 3969000

    def test_oxygen_generator_rating(self, sample):
        arr = to_array(sample)
        assert oxygen_generator_rating(arr, 0) == "10111"

    def test_co2_scrubber_rating(self, sample):
        arr = to_array(sample)
        assert co2_scrubber_rating(arr, 0) == "01010"

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
