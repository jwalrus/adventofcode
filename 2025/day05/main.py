def part1(rs, xs):
    result = 0

    for x in xs:
        for (a, b) in rs:
            if a <= x <= b:
                result += 1
                break

    return result


def part2(rs):
    rs = [(a, b + 1) for a, b in sorted(rs)]  # make range exclusive for easier math
    A, B = (0, 0)
    result = 0
    for (a, b) in rs:
        if A <= a <= B:
            if b >= B:
                result += b - B
                A, B = A, b
        else:
            result += b - a
            A, B = a, b

    return result


if __name__ == "__main__":
    import sys

    with open(sys.argv[1], "r") as fh:
        content = fh.read()
        ranges, items = content.split("\n\n")
        ranges = (r.split("-") for r in ranges.split("\n"))
        ranges = [(int(a), int(b)) for a, b in ranges]
        items = [int(x) for x in items.split("\n")]

    print("part1", part1(ranges, items))
    print("part2", part2(ranges))
