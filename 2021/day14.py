import itertools as it
from collections import Counter
from functools import reduce

import pytest


def polymer_counts(counts, rules):
    c = Counter()
    for k, v in counts.items():
        if k in rules:
            new = rules[k]
            k1, k2 = k[0] + new, new + k[1]
            c[k1] = c[k1] + v
            c[k2] = c[k2] + v
        else:
            c[k] = v
    return c


def part1(puzzle, *, n=10):
    polymer, rules = puzzle
    counts = Counter(("".join(p) for p in it.pairwise(polymer)))
    polymer = reduce(lambda acc, _: polymer_counts(acc, rules), range(n), counts)

    c = Counter()
    for k, v in polymer.items():
        one, two = k
        c[one] = c[one] + v
        c[two] = c[two] + v

    return (c.most_common()[0][1] - c.most_common()[-1][1]) // 2 + 1


def part2(puzzle):
    return part1(puzzle, n=40)


class TestDay14:

    def test_puzzle_input(self, sample, puzzle):
        assert sample[0] == "NNCB"
        assert len(sample[1]) == 16
        assert puzzle[0] == "PHVCVBFHCVPFKBNHKNBO"
        assert len(puzzle[1]) == 100

    def test_part1_sample(self, sample):
        assert part1(sample) == 1588

    def test_part1(self, puzzle):
        assert part1(puzzle) == 3555

    def test_part2_sample(self, sample):
        assert part2(sample) == 2188189693529

    def test_part2(self, puzzle):
        assert part2(puzzle) == 4439442043739


def parse_input(text):
    start, rules = text.strip().split("\n\n")
    rules = [x.strip() for x in rules.split("\n") if x != ""]
    rules = [x.strip().split(" -> ") for x in rules if x != ""]
    rules = {k: v for k, v in rules}
    return start, rules


@pytest.fixture(scope="module")
def puzzle():
    with open("day14.txt") as f:
        return parse_input(f.read())


@pytest.fixture(scope="module")
def sample():
    from textwrap import dedent
    return parse_input(dedent("""\
        NNCB
        
        CH -> B
        HH -> N
        CB -> H
        NH -> C
        HB -> C
        HC -> B
        HN -> C
        NN -> C
        BH -> H
        NC -> B
        NB -> B
        BN -> B
        BB -> N
        BC -> B
        CC -> N
        CN -> C
    """))
