import sys
from collections import deque


def main():
    with open(sys.argv[1]) as fh:
        racetrack = fh.read().splitlines()

    start, finish = (0, 0), (0, 0)
    for r, row in enumerate(racetrack):
        for c, val in enumerate(row):
            if val == "S":
                start = (r, c)
            if val == "E":
                finish = (r, c)

    print("part1:", run(racetrack, start, finish, pause=2, cutoff=100))
    print("part2:", run(racetrack, start, finish, pause=20, cutoff=100))


def run(racetrack, start, finish, *, pause, cutoff):
    path = bfs(racetrack, start, finish)
    shortcuts = []
    N = len(path)
    for i in range(N):
        for j in range(i + 1, N):
            dist = manhattan(path[i], path[j])
            savings = j - i - dist
            if dist <= pause and savings >= cutoff:
                shortcuts.append(savings)

    return len(shortcuts)


def manhattan(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def bfs(racetrack, start, finish):
    queue = deque([])
    queue.append((start, [start]))
    visited = set()

    while queue:
        cur, path = queue.popleft()
        if cur in visited:
            continue
        visited.add(cur)

        if cur == finish:
            return path

        r, c = cur
        for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            nr, nc = r + dr, c + dc
            if racetrack[nr][nc] != "#":
                queue.append(((nr, nc), path + [(nr, nc)]))

    return None


if __name__ == '__main__':
    main()
