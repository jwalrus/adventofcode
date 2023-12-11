import itertools
import re
from functools import reduce


def part1(start, instructions, nodes, *, f=lambda c: c == "ZZZ"):
    cur = start
    for i, instruction in enumerate(itertools.cycle(instructions)):
        choices = nodes[cur]
        match instruction:
            case "L":
                cur = choices[0]
            case "R":
                cur = choices[1]
        if f(cur):
            return i + 1


def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b // gcd(a, b)


def part2(instructions, nodes):
    locs = [node for node in nodes.keys() if node[-1] == "A"]
    ends = [part1(loc, instructions, nodes, f=lambda s: s.endswith("Z")) for loc in locs]
    return reduce(lcm, ends)


def main():
    with open(0) as f:
        instructions, _, *nodes = f.read().splitlines()
    nodes = [[x for x in re.findall(r"[A-Z0-9]+", node)] for node in nodes]
    nodes = {x: tuple(xs) for x, *xs in nodes}
    print("A:", part1("AAA", instructions, nodes))  # 13,019
    print("B:", part2(instructions, nodes))  # 13,524,038,372,771


if __name__ == "__main__":
    main()