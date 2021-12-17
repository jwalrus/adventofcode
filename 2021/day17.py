from bisect import bisect_left
from typing import List, Set, Tuple

import pytest

Point = Tuple[int, int]
TargetArea = Set[Point]
Path = List[Point]

bins = [(x * (x + 1) // 2) for x in range(200)]


def make_target_area(*, p1: Point, p2: Point) -> TargetArea:
    return {(a, b)
            for a in range(p1[0], p2[0] + 1)
            for b in range(p2[1], p1[1] + 1)}


def x_velocity_range(x1: int, x2: int) -> Tuple[int, int]:
    mn = bisect_left(bins, x1) - 1
    mx = bisect_left(bins, x2)
    return mn, mx


def path(dx: int, dy: int, *, x_max, y_min) -> Path:
    x, y = 0, 0
    points = [(0, 0)]
    while x <= x_max and y >= y_min:
        x, y = x + dx, y + dy
        points.append((x, y))
        dx = dx - 1 if dx > 0 else 0  # don't need to handle negative case here
        dy = dy - 1
    return points


def max_height_trajectories(p1: Point, p2: Point):
    x_min, x_max = x_velocity_range(p1[0], p2[0])
    y_min = p2[1]

    for x in range(x_min, x_max + 1):
        for y in range(0, abs(y_min) + 1):
            yield x, abs(y)


def all_trajectories(p1, p2):
    x_max, y_min = p2
    for x in range(x_max + 1):
        for y in range(y_min, abs(y_min) + 1):
            yield x, y


def success_paths(p1, p2, trajectories):
    results = []
    target = make_target_area(p1=p1, p2=p2)
    for dx, dy in trajectories(p1, p2):
        p = path(dx, dy, x_max=p2[0], y_min=p2[1])
        if set(p).intersection(target):
            results.append(((dx, dy), p))
    return results


def part1(puzzle):
    p1, p2 = puzzle
    results = success_paths(p1, p2, max_height_trajectories)

    mx_height = 0
    mx_velocity = None
    for v, p in results:
        h = max(x[1] for x in p)
        if h > mx_height:
            mx_height = h
            mx_velocity = v

    return mx_height


def part2(puzzle):
    p1, p2 = puzzle
    return len(success_paths(p1, p2, all_trajectories))


class TestDay17:

    def test_make_target_area(self, sample):
        assert len(make_target_area(p1=sample[0], p2=sample[1])) == 66

    def test_x_range(self, sample):
        mn, mx = x_velocity_range(sample[0][0], sample[1][0])
        assert mn == 5
        assert mx == 8

    def test_path(self):
        assert path(dx=7, dy=2, x_max=30, y_min=-10) == [
            (0, 0), (7, 2), (13, 3), (18, 3), (22, 2),
            (25, 0), (27, -3), (28, -7), (28, -12)
        ]

    def test_part1_sample(self, sample):
        assert part1(sample) == 45

    def test_part1(self, puzzle):
        assert part1(puzzle) == 8256

    def test_part2_sample(self, sample):
        assert part2(sample) == 112

    def test_part2(self, puzzle):
        assert part2(puzzle) == 2326


def parse_input(text):
    lines = [list(line.strip()) for line in text.split("\n") if line != ""]
    return [[int(x) for x in line] for line in lines]


@pytest.fixture(scope="module")
def puzzle():
    # target area: x=150..171, y=-129..-70
    return (150, -70), (171, -129)


@pytest.fixture(scope="module")
def sample():
    # target area: x=20..30, y=-10..-5
    return (20, -5), (30, -10)
