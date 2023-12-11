import re
import sys
from collections import defaultdict


def part1(lines, symbols):
    result = 0

    for row, line in enumerate(lines):
        for digit in re.finditer(r"\d+", line):
            (cs, ce), i = digit.span(), int(digit.group())
            cans = (
                    [(row - 1, c) for c in range(cs - 1, ce + 1)] +
                    [(row + 1, c) for c in range(cs - 1, ce + 1)] +
                    [(row, cs - 1), (row, ce)]
            )

            if any(can in symbols for can in cans):
                result += i

    return result


def part2(lines, gears):
    results = defaultdict(list)

    for row, line in enumerate(lines):
        for digit in re.finditer(r"\d+", line):
            (cs, ce), i = digit.span(), int(digit.group())
            cans = (
                    [(row - 1, c) for c in range(cs - 1, ce + 1)] +
                    [(row + 1, c) for c in range(cs - 1, ce + 1)] +
                    [(row, cs - 1), (row, ce)]
            )

            for can in cans:
                if can in gears:
                    results[can].append(i)

    return sum(xs[0] * xs[1] for _, xs in results.items() if len(xs) == 2)


def main():
    lines = sys.stdin.read().splitlines()
    symbols = {
        (row, col): char
        for row, line in enumerate(lines)
        for col, char in enumerate(line)
        if not char.isdigit() and char != "."
    }
    print("A:", part1(lines, symbols))  # 540,025

    gears = {rc for rc, char in symbols.items() if char == "*"}
    print("B:", part2(lines, gears))  # 84,584,891


if __name__ == '__main__':
    main()
