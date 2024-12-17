import heapq
import sys

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def part1(maze, start, end):
    visited = {}
    pq = [(0, start, RIGHT, [start])]
    min_score = 999999999999
    best = set()

    while pq:
        score, pos, dr, path = heapq.heappop(pq)
        visited[(pos, dr)] = score

        if score > min_score:
            break

        if pos == end:
            if score < min_score:
                best.clear()
                min_score = score
            best = best | set(path)

        st = straight(pos, dr)
        cw = clockwise(pos, dr)
        ct = counter_clockwise(pos, dr)

        if maze[st[0][0]][st[0][1]] != '#' and st not in visited:
            heapq.heappush(pq, (score + 1, st[0], st[1], path + [st[0]]))
        if maze[cw[0][0]][cw[0][1]] != '#' and cw not in visited:
            heapq.heappush(pq, (score + 1000, cw[0], cw[1], path + [cw[0]]))
        if maze[ct[0][0]][ct[0][1]] != '#' and ct not in visited:
            heapq.heappush(pq, (score + 1000, ct[0], ct[1], path + [ct[0]]))

    return min_score, len(best)


def clockwise(p, d):
    r, c = p
    if d == UP:
        return (r, c), RIGHT
    if d == RIGHT:
        return (r, c), DOWN
    if d == DOWN:
        return (r, c), LEFT
    if d == LEFT:
        return (r, c), UP


def counter_clockwise(p, d):
    r, c = p
    if d == UP:
        return (r, c), LEFT
    if d == LEFT:
        return (r, c), DOWN
    if d == DOWN:
        return (r, c), RIGHT
    if d == RIGHT:
        return (r, c), UP


def straight(p, d):
    r, c = p
    if d == UP:
        return (r - 1, c), UP
    if d == RIGHT:
        return (r, c + 1), RIGHT
    if d == DOWN:
        return (r + 1, c), DOWN
    if d == LEFT:
        return (r, c - 1), LEFT


if __name__ == '__main__':
    with open(sys.argv[1]) as fh:
        maze = fh.read().split("\n")
        R, C = len(maze), len(maze[0])
        S, E = (R - 2, 1), (1, C - 2)

    print(part1(maze, S, E))
