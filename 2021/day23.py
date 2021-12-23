import pytest

first_moves = {
    "A": {(0, 0), (0, 1), (0, 3), (0, 5), (0, 7), (0, 9), (0, 10)},
    "B": {(0, 0), (0, 1), (0, 3), (0, 5), (0, 7), (0, 9), (0, 10)},
    "C": {(0, 0), (0, 1), (0, 3), (0, 5), (0, 7), (0, 9), (0, 10)},
    "D": {(0, 0), (0, 1), (0, 3), (0, 5), (0, 7), (0, 9), (0, 10)},
}

second_moves = {
    "A": {(1, 2), (2, 2)},
    "B": {(1, 4), (2, 4)},
    "C": {(1, 6), (2, 6)},
    "D": {(1, 8), (2, 8)},
}


def part1(puzzle):
    return -1


def part2(puzzle):
    return -1


class TestDay23:

    def test_part1_sample(self, sample):
        assert part1(sample) == 0

    def test_part1(self, puzzle):
        assert part1(puzzle) == 0

    def test_part2_sample(self, sample):
        assert part2(sample) == 0

    def test_part2(self, puzzle):
        assert part2(puzzle) == 0


def parse_input(text):
    lines = [list(line.strip()) for line in text.split("\n") if line != ""]
    return [[int(x) for x in line] for line in lines]


@pytest.fixture(scope="module")
def puzzle():
    """
                 1
       01234567890
      #############
    0 #...........#
    1 ###C#C#B#D###
    2   #D#A#B#A#
        #########
    """
    return [
        ("A", (2, 8)),
        ("A", (2, 4)),
        ("B", (1, 6)),
        ("B", (2, 6)),
        ("C", (1, 2)),
        ("C", (1, 4)),
        ("D", (2, 2)),
        ("D", (1, 8)),
    ]


@pytest.fixture(scope="module")
def sample():
    """
                 1
       01234567890
      #############
    0 #...........#
    1 ###B#C#B#D###
    2   #A#D#C#A#
        #########
    """
    return [
        ("A", (2, 2)),
        ("A", (2, 8)),
        ("B", (1, 2)),
        ("B", (1, 6)),
        ("C", (1, 4)),
        ("C", (2, 6)),
        ("D", (2, 4)),
        ("D", (1, 8)),
    ]
