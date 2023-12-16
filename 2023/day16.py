from collections import deque


def right(row, col):
    return "R", (row, col + 1)


def left(row, col):
    return "L", (row, col - 1)


def down(row, col):
    return "D", (row + 1, col)


def up(row, col):
    return "U", (row - 1, col)


def empty_space(enter_from_direction, point):
    match enter_from_direction:
        case "R":
            return [right(*point)]
        case "L":
            return [left(*point)]
        case "D":
            return [down(*point)]
        case "U":
            return [up(*point)]


# /
def forward_slash(enter_from_direction, point):
    match enter_from_direction:
        case "R":
            return [up(*point)]
        case "L":
            return [down(*point)]
        case "D":
            return [left(*point)]
        case "U":
            return [right(*point)]


# \
def back_slash(enter_from_direction, point):
    match enter_from_direction:
        case "R":
            return [down(*point)]
        case "L":
            return [up(*point)]
        case "D":
            return [right(*point)]
        case "U":
            return [left(*point)]


# -
def dash(enter_from_direction, point):
    match enter_from_direction:
        case "R":
            return [right(*point)]
        case "L":
            return [left(*point)]
        case "D":
            return [left(*point), right(*point)]
        case "U":
            return [left(*point), right(*point)]


# |
def bar(enter_from_direction, point):
    match enter_from_direction:
        case "R":
            return [up(*point), down(*point)]
        case "L":
            return [up(*point), down(*point)]
        case "D":
            return [down(*point)]
        case "U":
            return [up(*point)]


def part1(grid, d="R", start=(0, 0)):
    ff = {
        ".": empty_space,
        "/": forward_slash,
        "\\": back_slash,
        "-": dash,
        "|": bar,
    }

    visited = set()
    stack = deque()
    stack.append((d, start))

    while stack:
        d, point = stack.pop()

        symbol = grid.get(point)
        if symbol is None:
            continue

        visited.add((d, point))

        for nd, npoint in ff[symbol](d, point):
            if (nd, npoint) not in visited:
                stack.append((nd, npoint))

    return len({p for _, p in visited})


def part2(grid):
    n_row = max(r for r, _ in grid.keys()) + 1
    n_col = max(c for _, c in grid.keys()) + 1

    d = [("D", (0, c)) for c in range(n_col)]
    u = [("U", (n_row - 1, c)) for c in range(n_col)]
    l = [("L", (r, n_col - 1)) for r in range(n_row)]
    r = [("R", (r, 0)) for r in range(n_row)]

    return max(part1(grid, d, start) for d, start in d + u + l + r)


def main():
    with open(0) as f:
        grid = [[c for c in line] for line in f.read().splitlines()]

    grid = {(row, col): c for row, line in enumerate(grid) for col, c in enumerate(line)}

    print("A:", part1(grid))  # 7,242
    print("B:", part2(grid))  # 7,572


if __name__ == '__main__':
    main()
