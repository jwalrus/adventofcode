import sys


def main():
    with open(sys.argv[1], "r") as f:
        lines = f.read().split("\n")

    ws, bs = set(), set()
    for y, r in enumerate(lines):
        for x, c in enumerate(r):
            if c == "#":
                ws.add((x - 1, y - 1))
            if c == ">":
                bs.add((x - 1, y - 1, +1, 0))
            if c == "<":
                bs.add((x - 1, y - 1, -1, 0))
            if c == "^":
                bs.add((x - 1, y - 1, 0, -1))
            if c == "v":
                bs.add((x - 1, y - 1, 0, +1))

    X = max(x for x, y in ws)
    Y = max(y for x, y in ws)

    ws |= {(x, -2) for x in range(-1, 3)}
    ws |= {(x, Y + 1) for x in range(X + 1, X - 4, -1)}

    start = (0, -1)
    ext = (X - 1, Y)
    goals = [ext, start, ext]
    queue = {start}
    t = 0

    while goals:
        t = t + 1
        b = {((x + dx * t) % X, (y + dy * t) % Y) for x, y, dx, dy in bs}
        nx = {(x + dx, y + dy) for x, y in queue for dx, dy in [(0, 1), (0, -1), (-1, 0), (1, 0), (0, 0)]}
        queue = nx - b - ws

        if goals[0] in queue:
            goal = goals.pop(0)
            print(goal, t)
            queue = {goal}


if __name__ == "__main__":
    main()
