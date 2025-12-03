def run(xs, stop, n):
    start = 0
    result = []
    while stop < len(xs) + 1 and len(result) < n:
        tmp = xs[start:stop]
        ix = start + tmp.index(max(tmp))
        result.append(str(xs[ix]))
        start = ix + 1
        stop = stop + 1
    return int("".join(result))


def main(xs, n):
    result = 0
    for x in xs:
        r = run(x, stop=len(x) - n + 1, n=n)
        result += r
    return result


if __name__ == "__main__":
    import sys

    with open(sys.argv[1], "r") as fh:
        data = [[int(c) for c in line.strip()] for line in fh.readlines()]

    print("part1", main(data, 2))
    print("part2", main(data, 12))
