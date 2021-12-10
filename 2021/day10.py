import operator
from functools import reduce

import more_itertools as mit
import pytest

OPEN = ["(", "<", "{", "["]
CLOSE = [")", ">", "}", "]"]
GOOD = ["()", "<>", "{}", "[]"]


def corrupt_combos():
    combos = ["".join([o, c]) for o in OPEN for c in CLOSE]
    return frozenset(combo for combo in combos if combo not in GOOD)


def analyze(s, corrupt=corrupt_combos()):
    bad = mit.first_true(corrupt, pred=lambda c: c in s, default=None)
    if bad is not None:
        return "corrupt", bad[1]

    new = reduce(lambda acc, x: acc.replace(x, ""), GOOD, s)

    if new == "":
        return "success", ""
    elif new == s:
        return "incomplete", new
    else:
        return analyze(new)


def part1(puzzle):
    points = {")": 3, "]": 57, "}": 1197, ">": 25137}
    results = [analyze(c) for c in puzzle]
    corrupted = [c for r, c in results if r == "corrupt"]
    return reduce(operator.add, [points[c] for c in corrupted])


def part2(puzzle):
    points = {")": 1, "]": 2, "}": 3, ">": 4}
    mapping = {"(": ")", "<": ">", "[": "]", "{": "}"}

    def ending(s):
        return "".join(mapping[c] for c in s)

    def score(s):
        return reduce(lambda acc, x: acc * 5 + x, [points[c] for c in s], 0)

    results = [analyze(c) for c in puzzle]
    incomplete = [ending(reversed(s)) for r, s in results if r == "incomplete"]
    scores = sorted([score(s) for s in incomplete])
    return scores[len(scores) // 2]


class TestDay10:

    def test_puzzle_input(self, sample, puzzle):
        assert len(sample) == 10
        assert sample[-1] == "<{([{{}}[<[[[<>{}]]]>[]]"
        assert len(puzzle) == 90

    def test_corrupt_combos(self):
        assert corrupt_combos() == {'(>', '(}', '(]', '<)', '<}', '<]', '{)', '{>', '{]', '[)', '[>', '[}'}

    def test_analyze(self):
        assert analyze("()<{}>[]") == ("success", "")
        assert analyze("()<{}") == ("incomplete", "<")
        assert analyze("()<{}][]") == ("corrupt", "]")
        assert analyze("{([(<{}[<>[]}>{[]{[(<()>") == ("corrupt", "}")

    def test_part1_sample(self, sample):
        assert part1(sample) == 26397

    def test_part1(self, puzzle):
        assert part1(puzzle) == 370407

    def test_part2_sample(self, sample):
        assert part2(sample) == 288957

    def test_part2(self, puzzle):
        assert part2(puzzle) == 3249889609


def parse_input(text):
    return [x.strip() for x in text.split("\n") if x != ""]


@pytest.fixture(scope="module")
def puzzle():
    with open("day10.txt") as f:
        return parse_input(f.read())


@pytest.fixture(scope="module")
def sample():
    s = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""
    return parse_input(s)
