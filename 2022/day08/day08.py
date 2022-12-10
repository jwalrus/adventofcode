import sys
from functools import reduce
from operator import mul


def shorter(xs, tree) -> bool:
    return all(x < tree for x in xs)


def from_above(i, j, trees):
    return [trees[ii][j] for ii in range(i - 1, -1, -1)]


def from_below(i, j, trees):
    return [trees[ii][j] for ii in range(i + 1, len(trees))]


def from_right(i, j, trees):
    return [trees[i][jj] for jj in range(j + 1, len(trees[0]))]


def from_left(i, j, trees):
    return [trees[i][jj] for jj in range(j - 1, -1, -1)]


def visible(loc, tree, trees):
    return any([
        shorter(from_above(*loc, trees), tree),
        shorter(from_below(*loc, trees), tree),
        shorter(from_left(*loc, trees), tree),
        shorter(from_right(*loc, trees), tree),
    ])


def tree_score(xs, tree):
    result = 0
    for x in xs:
        result = result + 1
        if x >= tree:
            return result

    return result


def score(loc, tree, trees):
    scores = [
        tree_score(from_above(*loc, trees), tree),
        tree_score(from_below(*loc, trees), tree),
        tree_score(from_left(*loc, trees), tree),
        tree_score(from_right(*loc, trees), tree),
    ]
    return reduce(mul, scores)


def part1(trees):
    return len([
        (i, j)
        for i, row in enumerate(trees)
        for j, tree in enumerate(row)
        if visible((i, j), tree, trees)
    ])


def part2(trees):
    return max(
        score((i, j), tree, trees)
        for i, row in enumerate(trees)
        for j, tree in enumerate(row)
    )


def main():
    with open(sys.argv[1], "r") as f:
        lines = f.read().split("\n")
        trees = [[int(x) for x in line] for line in lines]
        print(f"part1: {part1(trees)}")  # 1840
        print(f"part2: {part2(trees)}")  # 405769


if __name__ == '__main__':
    main()
