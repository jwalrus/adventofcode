import itertools


def part1(xs):
    xs = [x.split() for x in xs]
    nums, ops = xs[:-1], xs[-1]
    n_row, n_col = len(nums), len(nums[0])

    result = 0
    for c in range(n_col):
        tmp = 0 if ops[c] == "+" else 1
        for r in range(n_row):
            n = int(nums[r][c])
            if ops[c] == "+":
                tmp += n
            else:
                tmp *= n
        result += tmp

    return result


def part2(xs):
    operators = xs[-1]
    tmp = [list(x) for _, x in itertools.groupby(operators, lambda c: c == " ")]
    operators = ["".join(a + b) for a, b in zip(tmp[:-1:2], tmp[1::2])]
    cuts = [len(o) for o in operators]
    nums = xs[:-1]
    n_row, n_col = len(nums), len(nums[0])

    start = 0
    container = []
    for op, cut, col in zip(operators, cuts, range(n_col)):
        foo = []
        for row in nums:
            foo.append(row[start:start + cut])
        container.append(foo)
        start += cut

    result = 0

    for op, arr in zip(operators, container):
        if all(s[-1] == " " for s in arr):
            arr = [s[:-1] for s in arr]

        n = max(len(s) for s in arr)

        tmp_result = 0 if op.strip() == "+" else 1
        for i in range(n):
            m = 0
            for s in arr:
                if s[i] != " ":
                    m = 10 * m + int(s[i])
            if op.strip() == "+":
                tmp_result = tmp_result + m
            else:
                tmp_result = tmp_result * m

        result += tmp_result

    return result


if __name__ == "__main__":
    import sys

    with open(sys.argv[1], "r") as fh:
        data = fh.read().splitlines()

    print("part1", part1(data))
    print("part2", part2(data))
