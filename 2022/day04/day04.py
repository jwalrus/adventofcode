import re
import sys


def part1(a1, b1, a2, b2):
    return a1 <= a2 <= b2 <= b1 or a2 <= a1 <= b1 <= b2


def part2(a1, b1, a2, b2):
    return a1 <= a2 <= b1 or a2 <= a1 <= b2


with open(sys.argv[1], "r") as f:
    intervals = [[int(x) for x in re.split(r"[-,]", line)] for line in f.read().split("\n")]
    print("part1:", sum(1 for i in intervals if part1(*i)))
    print("part2:", sum(1 for i in intervals if part2(*i)))
