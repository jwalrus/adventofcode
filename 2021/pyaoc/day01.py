import itertools


def load():
    with open("day01.txt") as f:
        xs = f.readlines()
        return [int(x) for x in xs]


def part1(puzzle):
    return sum([x > y for x, y in zip(puzzle[1:], puzzle[:-1])])


def windows(xs, n=3):
    for i, _ in enumerate(xs[:-n + 1]):
        yield list(itertools.islice(xs, i, i + n))


def part2(puzzle):
    return part1([sum(w) for w in windows(puzzle, n=3)])


class TestDay01:

    def test_part1_sample(self):
        assert part1([199, 200, 208, 210, 200, 207, 240, 269, 260, 263]) == 7

    def test_part1(self):
        assert part1(load()) == 1482

    def test_windows(self):
        assert list(windows([1, 2, 3, 4], n=2)) == [[1, 2], [2, 3], [3, 4]]
        assert list(windows([1, 2, 3, 4, 5], n=2)) == [[1, 2], [2, 3], [3, 4], [4, 5]]

    def test_part2_sample(self):
        assert part2([199, 200, 208, 210, 200, 207, 240, 269, 260, 263]) == 5

    def test_part2(self):
        assert part2(load()) == 1518
