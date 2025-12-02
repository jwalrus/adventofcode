import re


def part1(s):
    cut = len(s) // 2
    return s[:cut] == s[cut:]


def part2(s):
    return re.match(r"^(\d+)\1+$", s) is not None


def main(xs, invalid):
    count = 0

    for a, b in xs:
        for n in range(int(a), int(b) + 1):
            if invalid(str(n)):
                count += n

    return count


if __name__ == "__main__":
    import sys

    with open(sys.argv[1], "r") as fh:
        data = fh.read().strip("\n").split(",")
        data = [x.split("-") for x in data]

    print("part1", main(data, part1))
    print("part2", main(data, part2))
