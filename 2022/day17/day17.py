import sys

MAX_RIGHT = 6
MAX_LEFT = 0

LINE = ((0, 0), (0, 1), (0, 2), (0, 3))
PLUS = ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1))
L = ((0, 0), (0, 1), (0, 2), (1, 2), (2, 2))
BAR = ((0, 0), (1, 0), (2, 0), (3, 0))
BOX = ((0, 0), (0, 1), (1, 0), (1, 1))


def move_down(rock, taken):
    if any(r - 1 < 0 for r, _ in rock) or any((r - 1, c) in taken for r, c in rock):
        return None
    return tuple((r - 1, c) for r, c in rock)


def move_right(rock, taken):
    if any(c == MAX_RIGHT for _, c in rock) or any((r, c + 1) in taken for r, c in rock):
        return rock
    return tuple((r, c + 1) for r, c in rock)


def move_left(rock, taken):
    if any(c == MAX_LEFT for _, c in rock) or any((r, c - 1) in taken for r, c in rock):
        return rock
    return tuple((r, c - 1) for r, c in rock)


def rock_gen(n, bottom_pad=3, left_pad=2):
    generators = [LINE, PLUS, L, BAR, BOX]
    i = 0
    for _ in range(n):
        rock = generators[i]
        yield i, lambda floor: tuple((r + floor + 1 + bottom_pad, c + left_pad) for r, c in rock)
        i = (i + 1) % len(generators)


def jet_gen(jets):
    i = 0
    n = len(jets)
    while True:
        yield i, jets[i]
        i = (i + 1) % n


def state_hash(taken, n=20):
    hgt = max(r for r, _ in taken)
    result = []
    for row in range(hgt, hgt-n, -1):
        for c in range(7):
            if (row, c) in taken:
                result.append((row + n - hgt, c))

    return frozenset(result)


def part1(n):
    with open(sys.argv[1], "r") as f:
        jets = jet_gen(f.read().strip())

    taken = set()
    height_map = {}
    states = {}

    for nr, (ir, rock) in enumerate(rock_gen(n)):

        current_floor = -1 if not taken else max(r for r, _ in taken)
        rock = rock(current_floor)

        # limit taken to last 1000 rows
        taken = {(r, c) for r, c in taken if r > current_floor - 1000}

        while rock is not None:
            ij, jet = next(jets)

            if jet == "<":
                rock = move_left(rock, taken)
            else:
                rock = move_right(rock, taken)

            rock_p = move_down(rock, taken)
            if rock_p is None:
                taken = taken | set(rock)
                height_map[nr] = max(r for r, _ in taken)

                key = (ir, ij, state_hash(taken))
                if key in states:
                    x = states[key]
                    return (
                        height_map[x] +
                        (height_map[nr] - height_map[x]) * ((n - x) // (nr - x)) +
                        height_map[x + (n - x - (n-x)//(nr-x) * (nr-x))] - height_map[x]
                    )

                states[key] = nr
                break
            else:
                rock = rock_p

    return max(r for r, _ in taken) + 1


if __name__ == "__main__":
    print("part1:", part1(2022))  # 3177
    print("part2:", part1(1000000000000))  # 1565517241382

