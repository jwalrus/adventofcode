import numpy as np


def load():
    with open("day01.txt") as f:
        xs = f.readlines()
        return [int(x) for x in xs]


def part1(puzzle, n=1):
    return sum([x > y for x, y in zip(puzzle[n:], puzzle[:-n])])


def part2(puzzle):
    # a + b + c < b + c + d => a < d
    return part1(puzzle, n=3)


def part1_np(arr: np.array, n=1):
    return np.sum(arr[n:] > arr[:-n])


def part2_np(arr: np.array):
    return part1_np(arr, n=3)


class TestDay01:

    def test_part1_sample(self):
        assert part1([199, 200, 208, 210, 200, 207, 240, 269, 260, 263]) == 7

    def test_part1(self):
        assert part1(load()) == 1482

    def test_part2_sample(self):
        assert part2([199, 200, 208, 210, 200, 207, 240, 269, 260, 263]) == 5

    def test_part2(self):
        assert part2(load()) == 1518

    def test_part1_np(self):
        assert part1(np.array(load())) == 1482

    def test_part2_np(self):
        assert part2(np.array(load())) == 1518
