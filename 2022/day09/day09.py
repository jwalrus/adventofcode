import sys

within_one = [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1]]


def dist(h, t):
    hx, hy = h
    tx, ty = t
    return ((hx - tx) ** 2 + (hy - ty) ** 2) ** 0.5


def moves(i, j, dr, n):
    match dr:
        case "R":
            return [(i + k, j) for k in range(1, n + 1)]
        case "L":
            return [(i - k, j) for k in range(1, n + 1)]
        case "U":
            return [(i, j + k) for k in range(1, n + 1)]
        case "D":
            return [(i, j - k) for k in range(1, n + 1)]
        case _:
            raise ValueError(f"what is this?!? {dr}")


def move_t(h, t):
    tx, ty = t
    possible = [(tx + x, ty + y) for x, y in within_one]
    one = [p for p in possible if dist(h, p) == 1]
    if one:
        return one[0]
    else:
        return [p for p in possible if dist(h, p) < 1.5][0]


def simulate(lines, num_knots):
    H = [(0, 0)]

    for d, n in lines:
        cur = H[-1]
        for move in moves(*cur, d, n):
            H.append(move)

    for _ in range(num_knots - 1):
        T = [(0, 0)]
        for i, h in enumerate(H):
            if dist(h, T[-1]) > 1.5:
                T.append(move_t(h, T[-1]))
        H = list(T)

    return len(set(H))


def main():
    with open(sys.argv[1], "r") as f:
        lines = [line.split(" ") for line in f.read().split("\n")]
        lines = [(d, int(n)) for d, n in lines]
        print("part1:", simulate(lines, 2))  # 6044
        print("part2:", simulate(lines, 10))  # 2384


if __name__ == '__main__':
    main()
