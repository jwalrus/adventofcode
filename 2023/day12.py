from functools import cache


# REF: https://github.com/xHyroM/aoc/blob/main/2023/12/second.py

@cache
def counts(xs, signature) -> int:
    # all inputs are processed
    if not xs:
        return 1 if len(signature) == 0 else 0

    # signature is exhausted and no "#" remains
    if not signature:
        return 1 if "#" not in xs else 0

    # accumulator
    result = 0

    # branch where ? is set to "."
    if xs[0] in ".?":
        # advance one character forward
        result += counts(xs[1:], signature)

    # branch where ? is set to "#"
    if (
            xs[0] in "#?"
            and signature[0] <= len(xs)  # still enough space to satisfy signature
            and "." not in xs[:signature[0]]  # can satisfy conditions in single block
            and
            (
                    signature[0] == len(xs)  # the remaining chars are the last signature
                    or xs[signature[0]] != "#"  # character after signature block is not a "#"
            )
    ):
        # advance one "set" forward
        result += counts(xs[signature[0] + 1:], signature[1:])

    return result


def part1(lines):
    result = 0
    for line in lines:
        symbols, signature = line.split()
        symbols, signature = symbols, tuple(map(int, signature.split(",")))
        result += counts(symbols, signature)
    return result


def part2(lines):
    result = 0
    for line in lines:
        symbols, signature = line.split()
        symbols, signature = "?".join([symbols] * 5), tuple(map(int, signature.split(","))) * 5
        result += counts(symbols, signature)
    return result


def main():
    with open(0) as f:
        lines = f.read().splitlines()
    print("A:", part1(lines))  # 7,236
    print("B:", part2(lines))  # 11,607,695,322,318


if __name__ == '__main__':
    main()
