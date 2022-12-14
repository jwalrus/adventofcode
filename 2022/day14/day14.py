import sys
from ast import literal_eval
from functools import reduce


def pairs(xs):
    return list(zip(xs[:-1], xs[1:]))


def rock_path(a, b):
    ax, ay = a
    bx, by = b
    if ax == bx:  # vertical line
        bot, top = min(ay, by), max(ay, by)
        return {(ax, i) for i in range(bot, top + 1)}
    else:
        lft, rgt = min(ax, bx), max(ax, bx)
        return {(i, ay) for i in range(lft, rgt + 1)}


def build_map(rocks) -> set:
    paths = (rock_path(*p) for r in rocks for p in pairs(r))
    return set(reduce(set.union, paths, set()))


def map_bounds(rmap):
    max_y = max(y for _, y in rmap)
    min_x = min(x for x, _ in rmap)
    max_x = max(x for x, _ in rmap)
    return min_x, max_x, 0, max_y


def sand_candidates(x, y):
    return [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]


def sand_path(start, rocks, sand, in_bounds):
    while in_bounds(start):
        prev_start = start
        for c in sand_candidates(*start):
            if c not in sand and c not in rocks:
                start = c
                break
        if start == prev_start:
            return start

    return -1, -1


def run(rock_map, sand_start, sentinel, in_bounds):
    sand = set()
    last_sand = (0, 0)

    while last_sand != sentinel:
        last_sand = sand_path(sand_start, rock_map, sand, in_bounds)

        if last_sand == sentinel:
            break
        else:
            sand.add(last_sand)

        # for y in range(10):
        #     print(y, " ", end="")
        #     for x in range(494, 504):
        #         if (x, y) in rock_map:
        #             print("#", end="")
        #         elif (x, y) in sand:
        #             print("o", end="")
        #         else:
        #             print(".", end="")
        #     print()
        # print()

    return len(sand)


def part1(rocks, sand_start=(500, 0), sentinel=(-1, -1)):
    rock_map = build_map(rocks)  # type: set
    x_min, x_max, y_min, y_max = map_bounds(rock_map)
    return run(
        rock_map, sand_start, sentinel,
        lambda p: x_min <= p[0] <= x_max and y_min <= p[1] <= y_max
    )


def part2(rocks, sand_start=(500, 0), sentinel=(500, 0)):
    rock_map = build_map(rocks)  # type: set
    _, _, y_min, y_max = map_bounds(rock_map)
    rock_map = rock_map.union({(x, y_max + 2) for x in range(-10_000, 10_000)})  # add floor
    return 1 + run(
        rock_map, sand_start, sentinel,
        lambda _: True
    )


def main():
    with open(sys.argv[1], "r") as f:
        rocks = [
            [literal_eval(x) for x in line.split(" -> ")]
            for line in (f.read().split("\n"))
        ]
        print("part1:", part1(rocks))  # 892
        print("part2:", part2(rocks))  # 27155


if __name__ == "__main__":
    main()
