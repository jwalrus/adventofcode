import textwrap

import pytest

X = 0
Y = 1


def gridify(dots):
    max_x = max(t[0] for t in dots) + 1
    max_y = max(t[1] for t in dots) + 1
    return [[1 if (x, y) in dots else 0 for x in range(max_x)] for y in range(max_y)]


def printable_grid(dots, marker="\u2588"):
    grid = gridify(dots)
    return "\n".join(["".join([marker if x else "." for x in line]) for line in grid])


def fold_left(dots, i):
    left_dots = {dot for dot in dots if dot[X] < i}
    right_dots = {dot for dot in dots if dot[X] > i}

    mid = max(dot[X] for dot in dots) / 2
    if i >= mid:  # left side is larger
        right_dots = {(i - (x - i), y) for x, y in right_dots}
        return left_dots.union(right_dots)
    else:
        left_dots = {(x + i + 1, y) for x, y in left_dots}
        return {(x - (i + 1), y) for x, y in right_dots.union(left_dots)}  # reindex dots


def fold_up(dots, i):
    flipped = {(y, x) for x, y in dots}
    flipped_dots = fold_left(flipped, i)
    return {(x, y) for y, x in flipped_dots}


def fold(dots, instruction):
    match instruction:
        case ("x", x):
            return fold_left(dots, x)
        case ("y", y):
            return fold_up(dots, y)


def part1(puzzle):
    dots, instructions = puzzle
    return len(fold(dots, instructions[0]))


def part2(puzzle):
    dots, instructions = puzzle
    for i, instruction in enumerate(instructions):
        dots = fold(dots, instruction)
    return printable_grid(dots)


class TestDay13:

    def test_puzzle_input(self, sample, puzzle):
        s_dots, s_instructions = sample
        assert len(s_dots) == 18
        assert len(s_instructions) == 2

        p_dots, p_instructions = puzzle
        assert len(p_dots) == 887
        assert len(p_instructions) == 12

    def test_gridify(self, sample):
        dots = [(0, 0), (1, 1), (2, 2), (2, 0)]
        assert gridify(dots) == [
            [1, 0, 1],
            [0, 1, 0],
            [0, 0, 1],
        ]
        dots = [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]
        assert gridify(dots) == [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1],
        ]
        print(printable_grid(gridify(sample[0])))

    def test_fold_left(self):
        dots = {(1, 0), (2, 0), (5, 0)}
        assert fold_left(dots, 4) == {(1, 0), (2, 0), (3, 0)}
        assert fold_left(dots, 1) == {(0, 0), (3, 0)}
        assert fold_left(dots, 3) == {(1, 0), (2, 0)}
        assert fold_left(dots, 2) == {(1, 0), (2, 0)}

        assert fold_left({(1, 0), (8, 0)}, 4) == {(0, 0), (1, 0)}, "FOO"

    def test_fold_up(self):
        dots = {(0, 1), (0, 2), (0, 5)}
        assert fold_up(dots, 4) == {(0, 1), (0, 2), (0, 3)}
        assert fold_up(dots, 1) == {(0, 0), (0, 3)}
        assert fold_up(dots, 3) == {(0, 1), (0, 2)}
        assert fold_up(dots, 2) == {(0, 1), (0, 2)}

    def test_part1_sample(self, sample):
        assert part1(sample) == 17

    def test_part1(self, puzzle):
        assert part1(puzzle) == 755

    def test_part2_sample(self, sample):
        assert part2(sample) == textwrap.dedent("""\
        █████
        █...█
        █...█
        █...█
        █████""")

    def test_part2(self, puzzle):
        assert part2(puzzle) == textwrap.dedent("""\
        ███..█....█..█...██.███..███...██...██.
        █..█.█....█.█.....█.█..█.█..█.█..█.█..█
        ███..█....██......█.█..█.███..█..█.█...
        █..█.█....█.█.....█.███..█..█.████.█.██
        █..█.█....█.█..█..█.█.█..█..█.█..█.█..█
        ███..████.█..█..██..█..█.███..█..█..███""")


def parse_input(text):
    dots, instructions = text.split("\n\n")

    dots = [x for x in dots.split("\n") if x != ""]
    dots = [x.strip().split(",") for x in dots]
    dots = [(int(x), int(y)) for x, y in dots]

    instructions = [x for x in instructions.split("\n") if x != ""]
    instructions = [x.strip().replace("fold along ", "").split("=") for x in instructions]
    instructions = [(x, int(y)) for x, y in instructions]

    return dots, instructions


@pytest.fixture(scope="module")
def puzzle():
    with open("day13.txt") as f:
        return parse_input(f.read())


@pytest.fixture(scope="module")
def sample():
    from textwrap import dedent
    return parse_input(dedent("""\
        6,10
        0,14
        9,10
        0,3
        10,4
        4,11
        6,0
        6,12
        4,1
        0,13
        10,12
        3,4
        3,0
        8,4
        1,10
        2,14
        8,10
        9,0
        
        fold along y=7
        fold along x=5
    """))
