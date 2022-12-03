import string
import sys
from functools import reduce


def priority(c):
    if c in string.ascii_lowercase:
        return ord(c) - 96
    else:
        return ord(c) - (65 - 27)


with open(sys.argv[1], "r") as f:
    lines = f.read().split("\n")

    cuts = ((set(x[:len(x) // 2]), set(x[len(x) // 2:])) for x in lines)
    print("part1:", sum(priority(min(a & b)) for a, b in cuts))

    groups = (map(set, lines[i * 3:i * 3 + 3]) for i in range(len(lines) // 3))
    print("part2:", sum(priority(min(reduce(set.intersection, group))) for group in groups))
