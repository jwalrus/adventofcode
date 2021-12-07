import more_itertools as mit
import pytest


def cost(crabs, pos, *, cost_to_move):
    return sum(cost_to_move(crab, pos) for crab in crabs)


def part1(puzzle, func=lambda a, b: abs(a - b)):
    mn, mx = mit.minmax(puzzle)
    return min(cost(puzzle, pos, cost_to_move=func) for pos in range(mn, mx + 1))


def part2(puzzle):
    return part1(puzzle, func=lambda a, b: int(abs(a - b) * (abs(a - b) + 1) / 2))


class TestDay07:

    def test_puzzle_input(self, sample, puzzle):
        assert sample == [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
        assert len(puzzle) == 1000

    def test_cost(self, sample):
        f = lambda a, b: abs(a - b)
        assert cost(sample, 1, cost_to_move=f) == 41
        assert cost(sample, 2, cost_to_move=f) == 37
        assert cost(sample, 3, cost_to_move=f) == 39
        assert cost(sample, 10, cost_to_move=f) == 71

    def test_inc_cost(self, sample):
        f = lambda a, b: int(abs(a - b) * (abs(a - b) + 1) / 2)
        assert cost(sample, 2, cost_to_move=f) == 206
        assert cost(sample, 5, cost_to_move=f) == 168

    def test_part1_sample(self, sample):
        assert part1(sample) == 37

    def test_part1(self, puzzle):
        assert part1(puzzle) == 342730

    def test_part2_sample(self, sample):
        assert part2(sample) == 168

    def test_part2(self, puzzle):
        assert part2(puzzle) == 92335207


def parse_input(text):
    return [int(x) for x in text.strip().split(',')]


@pytest.fixture(scope="module")
def puzzle():
    with open("day07.txt") as f:
        return parse_input(f.read())


@pytest.fixture(scope="module")
def sample():
    s = """16,1,2,0,4,2,7,1,2,14"""
    return parse_input(s)
