import pytest


def create_board(xs):
    board = {}
    for row, line in enumerate(xs):
        for col, value in enumerate(line):
            if value != ".":
                board[(row, col)] = value
    return board


def evolve(board, *, H, W):
    right = {position for position, direction in board.items() if direction == ">"}
    down = {position for position, direction in board.items() if direction == "v"}

    new_board = {}
    for row, col in right:
        new_pos = (row, (col + 1) % W)
        if new_pos not in board:
            new_board[new_pos] = ">"
        else:
            new_board[(row, col)] = ">"

    for row, col in down:
        new_pos = (((row + 1) % H), col)
        if new_pos not in new_board and board.get(new_pos) != "v":
            new_board[new_pos] = "v"
        else:
            new_board[(row, col)] = "v"

    return new_board


def part1(puzzle):
    H = len(puzzle)
    W = len(puzzle[0])
    board0 = create_board(puzzle)
    i = 0
    while True:
        i, board1 = i + 1, evolve(board0, H=H, W=W)
        if board0 == board1:
            return i
        else:
            board0 = board1


def part2(puzzle):
    return -1


class TestDay25:

    def test_puzzle_input(self, sample, puzzle):
        assert len(sample) == 9
        assert len(sample[0]) == 10
        assert len(puzzle) == 137
        assert len(puzzle[0]) == 139

    def test_create_board(self):
        assert create_board([[">", "."], [".", "v"]]) == {(1, 1): "v", (0, 0): ">"}

    def test_part1_sample(self, sample):
        assert part1(sample) == 58

    def test_part1(self, puzzle):
        assert part1(puzzle) == 509


def parse_input(text):
    lines = [x.strip() for x in text.split("\n") if x != ""]
    return [list(line) for line in lines]


@pytest.fixture(scope="module")
def puzzle():
    with open("day25.txt") as f:
        return parse_input(f.read())


@pytest.fixture(scope="module")
def sample():
    from textwrap import dedent
    return parse_input(dedent("""\
        v...>>.vv>
        .vv>>.vv..
        >>.>v>...v
        >>v>>.>.v.
        v>v.vv.v..
        >.>>..v...
        .vv..>.>v.
        v.v..>>v.v
        ....v..v.>
    """))
