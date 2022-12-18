import sys
from collections import deque

X, Y, Z = 0, 1, 2


def neighbors(x, y, z):
    return {
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    }


def part1(cubes):
    return sum(len(neighbors(*cube) - cubes) for cube in cubes)


def part2(cubes):
    x_min, x_max = min(c[X] for c in cubes), max(c[X] for c in cubes)
    y_min, y_max = min(c[Y] for c in cubes), max(c[Y] for c in cubes)
    z_min, z_max = min(c[Z] for c in cubes), max(c[Z] for c in cubes)

    air = {
              (x, y, z)
              for x in range(x_min - 1, x_max + 2)
              for y in range(y_min - 1, y_max + 2)
              for z in range(z_min - 1, z_max + 2)
          } - cubes

    start = (x_min - 1, y_min - 1, z_min - 1)

    stack = deque([start])
    found = {start}

    while stack:
        cur = stack.pop()
        ns = neighbors(*cur)
        for n in ns:
            if n not in found and n not in cubes and n in air:
                found.add(n)
                stack.append(n)

    return part1(cubes) - part1(air - found)


def main():
    with open(sys.argv[1], "r") as f:
        lines = [line.split(",") for line in f.read().split("\n")]
        cubes = {(int(x), int(y), int(z)) for x, y, z in lines}
        print("part1:", part1(cubes))  # 4332
        print("part2:", part2(cubes))  # 2524


if __name__ == "__main__":
    main()
