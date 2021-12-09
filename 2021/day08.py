import itertools as it
from typing import Iterable

import more_itertools as mit
import pytest


def build_entry(s):
    vals = frozenset(s)
    match len(s):
        case 2:
            return 1, vals
        case 3:
            return 7, vals
        case 4:
            return 4, vals
        case 7:
            return 8, vals
        case _:
            raise ValueError(f"Only handles strings of length 2, 3, 4, or 7. Received {s=}")


def nine(x, known) -> bool:
    return len(x) == 6 and known[4].difference(x) == set()


def six(x, known) -> bool:
    return len(x) == 6 and known[4].difference(x) != set() and known[1].difference(x) != set()


def zero(x, known) -> bool:
    return len(x) == 6 and known[4].difference(x) != set() and known[1].difference(x) == set()


def three(x, known) -> bool:
    return len(x) == 5 and known[7].difference(x) == set()


def five(x, known) -> bool:
    return len(x) == 5 and x.difference(known[6]) == set()


def two(x, known) -> bool:
    return len(x) == 5 and x.difference(known[6]) != set() and known[7].difference(x) != set()


def build_mapping(in_: Iterable[str]):
    unknown = [frozenset(i) for i in in_ if len(i) in {5, 6}]
    known = {k: v for k, v in (build_entry(s) for s in in_ if len(s) not in {5, 6})}
    known[9] = mit.first_true(unknown, pred=lambda s: nine(s, known))
    known[6] = mit.first_true(unknown, pred=lambda s: six(s, known))
    known[0] = mit.first_true(unknown, pred=lambda s: zero(s, known))
    known[3] = mit.first_true(unknown, pred=lambda s: three(s, known))
    known[5] = mit.first_true(unknown, pred=lambda s: five(s, known))
    known[2] = mit.first_true(unknown, pred=lambda s: two(s, known))
    return {v: k for k, v in known.items()}


def part1(puzzle):
    output = it.chain.from_iterable((p[1] for p in puzzle))
    return sum((len(x) in {2, 3, 4, 7}) for x in output)


def part2(puzzle):
    result = 0
    for in_, out_ in puzzle:
        mapping = build_mapping(in_)
        values = [str(mapping[frozenset(x)]) for x in out_]
        result += int("".join(values))

    return result


class TestDay08:

    def test_puzzle_input(self, sample, puzzle):
        assert len(sample) == 10
        assert len(puzzle) == 200

    def test_part1_sample(self, sample):
        assert part1(sample) == 26

    def test_part1(self, puzzle):
        assert part1(puzzle) == 514

    def test_part2_sample(self, sample):
        assert part2(sample) == 61229

    def test_part2(self, puzzle):
        assert part2(puzzle) == 1012272


def parse_input(text):
    lines = [line.strip() for line in text.split("\n")]
    in_out = [tuple(line.split(" | ")) for line in lines]
    return [(i.split(" "), o.split(" ")) for i, o in in_out]


@pytest.fixture(scope="module")
def puzzle():
    with open("day08.txt") as f:
        return parse_input(f.read())


@pytest.fixture(scope="module")
def sample():
    s = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""
    return parse_input(s)
