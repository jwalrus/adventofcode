from collections import deque


def north(row, col):
    return row - 1, col


def south(row, col):
    return row + 1, col


def east(row, col):
    return row, col + 1


def west(row, col):
    return row, col - 1


def next_(parent, loc, sketch) -> tuple | None:
    n = north(*loc)
    s = south(*loc)
    e = east(*loc)
    w = west(*loc)
    match sketch.get(loc):
        case "|":
            if parent == n:
                return s
            elif parent == s:
                return n
            else:
                return None
        case "-":
            if parent == w:
                return e
            elif parent == e:
                return w
            else:
                return None
        case "L":
            if parent == n:
                return e
            elif parent == e:
                return n
            else:
                return None
        case "J":
            if parent == n:
                return w
            elif parent == w:
                return n
            else:
                return None
        case "7":
            if parent == s:
                return w
            elif parent == w:
                return s
            else:
                return None
        case "F":
            if parent == s:
                return e
            elif parent == e:
                return s
            else:
                return None
        case _:
            return None


def dfs(S, loc, sketch):
    stack = deque()
    stack.append((S, loc, 1))
    visited = set()
    while stack:
        parent, loc, depth = stack.pop()
        visited.add(loc)
        if sketch.get(loc) == "S":
            return visited
        nxt = next_(parent, loc, sketch)
        if nxt:
            stack.append((loc, nxt, depth + 1))

    return None


def part1(sketch):
    S = [loc for loc, val in sketch.items() if val == "S"][0]
    for loc in [north(*S), south(*S), east(*S), west(*S)]:
        visited = dfs(S, loc, sketch)
        if visited is not None:
            return visited

    return None


def find_right(loc, loop, sketch):
    e = east(*loc)
    if e not in sketch:
        return None
    if e in loop:
        return e
    return find_right(e, loop, sketch)


def is_cross(loc, loop, sketch):
    return sketch.get(loc) in {"F", "7", "|"} and loc in loop


def part2(sketch):
    # find loop
    loop = part1(sketch)
    nrow, ncol = max(x for x in sketch)
    count = 0
    interior = set()
    for row in range(nrow + 1):
        for col in range(ncol, -1, -1):

            if (row, col) not in loop:
                crosses = sum(1 for c in range(col, ncol + 1) if is_cross((row, c), loop, sketch))
                if crosses % 2 == 1:
                    print((row, col), crosses)
                    interior.add((row, col))
                    count += 1
    return count


def main():
    sketch = {}
    with open(0) as f:
        for row, line in enumerate(f):
            for col, c in enumerate(line.rstrip()):
                sketch[(row, col)] = c

    print("A:", len(part1(sketch)) // 2)  # 6882
    print("B:", part2(sketch))  # 491 too high


if __name__ == '__main__':
    main()
