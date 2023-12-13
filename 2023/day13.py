def rotate(grid):
    n_row, n_col = len(grid), len(grid[0])
    result = [list() for _ in range(n_col)]
    for row in range(n_row):
        for col in range(n_col):
            result[col].append(grid[row][col])
    return result


def reflection(xs, ys):
    return all(x == y for x, y in zip(xs[::-1], ys))


def smudge(xs, ys):
    return sum((a != b for x, y in zip(xs[::-1], ys) for a, b in zip(x, y))) == 1


def find(p, *, f):
    for c, _ in enumerate(p):
        left, right = p[:c], p[c:]
        if left and right:
            if f(left, right):
                return len(left)
    return 0


def calc(patterns, *, f):
    return sum(100 * find(p, f=f) + find(rotate(p), f=f) for p in patterns)


def main():
    with open(0) as f:
        patterns = [p.split("\n") for p in f.read().split("\n\n")]
    print("A:", calc(patterns, f=reflection))  # 37,561
    print("B:", calc(patterns, f=smudge))  # 31,108


if __name__ == "__main__":
    main()
