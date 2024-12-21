import sys
from collections import deque

NUMPAD = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [" ", "0", "A"],
]


KEYPAD = [
    [" ", "^", "A"],
    ["<", "v", ">"],
]

UP = ((-1,  0), "^")
DW = (( 1,  0), "v")
RT = (( 0,  1), ">")
LF = (( 0, -1), "<")


def main():
    with open(sys.argv[1]) as fh:
        codes = fh.read().splitlines()
    print("part1:", part1(codes))


def part1(codes):
    num_pos = (3, 2)
    key_pos = (0, 2)
    for code in codes:
        keystrokes = []
        for key in code:
            num_pos, key_pos, path = bfs(num_pos, key, key_pos, NUMPAD)
            keystrokes += path
            keystrokes += ["A"]
        print(keystrokes)
        print("".join(keystrokes))


def bfs(num_pos, num_target, key_pos, space):
    queue = deque()
    queue.append((num_pos, key_pos, []))
    visited = set()

    while queue:
        num_pos, key_pos, path = queue.popleft()
        if space[num_pos[0]][num_pos[1]] == num_target:
            return num_pos, key_pos, path
        if num_pos in visited:
            continue

        for d, sym in [UP, DW, RT, LF]:
            nr, nc = num_pos[0] + d[0], num_pos[1] + d[1]
            if nr < 0 or nc < 0 or nr >= len(space) or nc >= len(space[0]):
                continue
            queue.append(((nr, nc), key_pos, path + [sym]))

    raise ValueError("No solution found")




if __name__ == '__main__':
    main()