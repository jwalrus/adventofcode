import sys
from dataclasses import dataclass


@dataclass
class P:
    r: int
    c: int

    def __add__(self, other):
        return P(self.r + other.r, self.c + other.c)

    def __sub__(self, other):
        return P(self.r - other.r, self.c - other.c)


UP = P(r=-1, c=0)
RT = P(r=0, c=1)
DW = P(r=1, c=0)
LF = P(r=0, c=-1)

MOVES = {
    "<": LF,
    ">": RT,
    "^": UP,
    "v": DW,
}


def part1(warehouse, moves):
    cur = [P(r, c) for r, row in enumerate(warehouse) for c, val in enumerate(row) if val == "@"][0]

    for move in moves:
        d = MOVES[move]
        cur, warehouse = update(warehouse, cur, d)

    result = 0
    for r, row in enumerate(warehouse):
        for c, val in enumerate(row):
            if val == "O" or val == "[":
                result += 100 * r + c

    return result


def update(warehouse, point, d):
    arr = [list(row) for row in warehouse]

    def go(p):
        p = p + d
        if all([
            arr[p.r][p.c] != "[" or go(p + RT) and go(p),
            arr[p.r][p.c] != "]" or go(p + LF) and go(p),
            arr[p.r][p.c] != "O" or go(p),
            arr[p.r][p.c] != "#",
        ]):
            np = p - d
            arr[p.r][p.c], arr[np.r][np.c] = arr[np.r][np.c], arr[p.r][p.c]
            return True

    if go(point):
        return point + d, arr
    else:
        return point, warehouse


def main():
    with open(sys.argv[1]) as fh:
        raw_file = fh.read()

    warehouse, moves = raw_file.split('\n\n')
    warehouse = [[c for c in line] for line in warehouse.splitlines()]
    moves = moves.replace("\n", "")
    print("part1:", part1(warehouse, moves))

    warehouse, moves = raw_file.split('\n\n')
    warehouse = warehouse.replace("#", "##").replace(".", "..").replace("O", "[]").replace("@", "@.")
    warehouse = [[c for c in line] for line in warehouse.splitlines()]
    moves = moves.replace("\n", "")
    print("part2:", part1(warehouse, moves))


if __name__ == '__main__':
    main()
