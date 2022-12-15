import sys
from functools import reduce


def is_digit(x: str):
    if x == "":
        return False
    else:
        return x.isdigit() if x[0] != "-" else x[1:].isdigit()


def manhattan(ax, ay, bx, by):
    return abs(ax - bx) + abs(ay - by)


def on_row(sensor, beacon, y):
    delta = manhattan(*sensor, *beacon) - manhattan(*sensor, sensor[0], y)
    lx, rx = sensor[0] - delta, sensor[0] + delta
    return {(x, y) for x in range(lx, rx + 1)}


def border(sensor, beacon, bound):
    dist = manhattan(*sensor, *beacon) + 1
    x, y = sensor
    tl = [(x - dist + i, y + i) for i in range(dist + 1)]
    tr = [(x + dist - i, y + i) for i in range(dist + 1)]
    br = [(x + dist - i, y - i) for i in range(dist + 1)]
    bl = [(x - dist + i, y - i) for i in range(dist + 1)]
    return {(x, y) for x, y in set(tl + tr + br + bl) if 0 < x < bound and 0 < y < bound}


def part1(pairs, y=2_000_000):
    sensors = {s for s, _ in pairs}
    beacons = {b for _, b in pairs}
    filtered = [(s, b) for s, b in pairs if manhattan(*s, s[0], y) <= manhattan(*s, *b)]
    positions = set(reduce(set.union, [on_row(s, b, y) for s, b in filtered]))
    return len(positions.difference(sensors.union(beacons)))


def part2(pairs, bound=4_000_000):
    radii = {s: manhattan(*s, *b) for s, b in pairs}

    for s, b in pairs:
        coords = border(s, b, bound)
        for c in coords:
            if all(manhattan(*c, *ss) > radii[ss] for ss, _ in pairs):
                return 4_000_000 * c[0] + c[1]

    return -1


def main():
    with open(sys.argv[1], "r") as f:
        lines = [
            [int(x.strip(",:xy=")) for x in line.split(" ") if is_digit(x.strip(",:xy="))]
            for line in f.read().split("\n")
        ]
        pairs = [((a, b), (c, d)) for a, b, c, d in lines]
        print("part1:", part1(pairs, y=2_000_000))  # 5142231 (4.47s)
        print("part2:", part2(pairs, bound=4_000_000))  # 10884459367718 (9.13s)


if __name__ == "__main__":
    main()
