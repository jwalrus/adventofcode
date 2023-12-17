import heapq


def calc(grid, start, stop, minimum=1, maximum=3):
    # dijkstra (more or less) with min-heap (via heapq)
    heap = [(0, start[0], start[1], 0, 0)]  # (score, row, col, row_dir, col_dir)
    visited = set()

    while heap:
        score, row, col, d_row, d_col = heapq.heappop(heap)

        # exit if target is found
        if (row, col) == stop:
            return score

        # keep track visited blocks AND the direction from which they were entered
        if (row, col, d_row, d_col) in visited:
            continue
        visited.add((row, col, d_row, d_col))

        # visit neighbors
        # to keep track of min/max moves in given direction:
        #   1. don't allow moves in the direction your moving
        #   2. when you move a new direction, add max moves in common direction to min-heap
        # this prevents having to keep track of movement history and direction
        for dr, dc in {(0, 1), (0, -1), (-1, 0), (1, 0)} - {(d_row, d_col), (-d_row, -d_col)}:
            # copy of values to move along each vector
            ar, ac, ascore = row, col, score
            for i in range(1, minimum):
                ar, ac = ar + dr, ac + dc
                if (ar, ac) in grid:
                    ascore = ascore + grid[(ar, ac)]
            for i in range(minimum, maximum + 1):
                ar, ac = ar + dr, ac + dc
                if (ar, ac) in grid:
                    ascore = ascore + grid[(ar, ac)]
                    heapq.heappush(heap, (ascore, ar, ac, dr, dc))

    return -1


def main():
    with open(0) as f:
        grid = {
            (r, c): int(val)
            for r, row in enumerate(f.read().splitlines())
            for c, val in enumerate(row)
        }
    n_row = max(r for r, _ in grid)
    n_col = max(c for _, c in grid)
    print("A:", calc(grid, (0, 0), (n_row, n_col)))  # 861
    print("B:", calc(grid, (0, 0), (n_row, n_col), minimum=4, maximum=10))  # 1037


if __name__ == '__main__':
    main()
