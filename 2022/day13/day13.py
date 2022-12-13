import json
import sys

from functools import cmp_to_key


def zip_longest(xs, ys):
    mx = max(len(xs), len(ys))
    for i in range(mx):
        if i >= len(xs):
            yield None, ys[i]
        elif i >= len(ys):
            yield xs[i], None
        else:
            yield xs[i], ys[i]


def compare(left, right):
    def cmp(ll, rr):
        match isinstance(ll, list), isinstance(rr, list):
            case True, True:
                return compare(ll, rr)
            case True, False:
                return compare(ll, [rr])
            case False, True:
                return compare([ll], rr)
            case _:
                if ll < rr:
                    return -1
                elif ll == rr:
                    return 0
                else:
                    return 1

    left, right = list(left), list(right)
    for l, r in zip_longest(left, right):
        if l is None:
            return -1
        if r is None:
            return 1

        c = cmp(l, r)
        if c != 0:
            return c

    return 0


def part1(packets):
    pairs = enumerate(zip(packets[:-1:2], packets[1::2]))
    return sum(i + 1 for i, (l, r) in pairs if compare(l, r) <= 0)


def part2(packets):
    packets = sorted(packets + [[[2]], [[6]]], key=cmp_to_key(compare))
    idx = [i + 1 for i, p in enumerate(packets) if p == [[2]] or p == [[6]]]
    return idx[0] * idx[1]


def main():
    with open(sys.argv[1], "r") as f:
        packets = [json.loads(line) for line in f.read().split("\n") if line != ""]
        print("part1:", part1(packets))  # 5625
        print("part2:", part2(packets))  # 23111


if __name__ == "__main__":
    main()
