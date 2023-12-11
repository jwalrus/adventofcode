from itertools import combinations


def rotate(grid):
    n_row, n_col = len(grid), len(grid[0])
    result = [list() for _ in range(n_col)]
    for row in range(n_row):
        for col in range(n_col):
            result[col].append(grid[row][col])
    return result


def dist(a, b, empty_rows, empty_cols, *, scale):
    (ar, ac), (br, bc) = a, b
    er = sum(1 for r in empty_rows if min(ar, br) < r < max(ar, br))
    ec = sum(1 for c in empty_cols if min(ac, bc) < c < max(ac, bc))

    if er == 0 and ec == 0:
        pass

    result = abs(ar - br) + abs(ac - bc) + (er + ec) * (scale - 1)
    return result


def calc(image, scale):
    empty_rows = {i for i, line in enumerate(image) if all(c == "." for c in line)}
    empty_cols = {i for i, line in enumerate(rotate(image)) if all(c == "." for c in line)}
    galaxies = [(i, j) for i, row in enumerate(image) for j, col in enumerate(row) if col == "#"]
    return sum(dist(a, b, empty_rows, empty_cols, scale=scale) for a, b in combinations(galaxies, 2))


def main():
    with open(0) as f:
        image = f.read().splitlines()
    print("A:", calc(image, scale=2))  # 9,795,148
    print("B:", calc(image, scale=1000000))  # 650,672,493,820


if __name__ == '__main__':
    main()
