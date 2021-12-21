import itertools
from functools import cache


def deterministic_dice(n, start=1, stop=100):
    iterator = itertools.cycle(range(start, stop + 1))
    while True:
        yield list(itertools.islice(iterator, n))


def move(start, num) -> int:
    return (start + num) % 10


def score(position) -> int:
    return 10 if position == 0 else position


def part1(*, p1, p2):
    score_p1 = 0
    score_p2 = 0
    p1_turn = True
    rolls = deterministic_dice(3, start=1, stop=100)
    n = 0

    while score_p1 < 1000 and score_p2 < 1000:
        n += 3
        a, b, c = next(rolls)
        if p1_turn:
            p1 = move(p1, a + b + c)
            score_p1 += score(p1)
            p1_turn = False
        else:
            p2 = move(p2, a + b + c)
            score_p2 += score(p2)
            p1_turn = True

    return (score_p1 * n) if score_p1 < 1000 else (score_p2 * n)


def part2(*, p1, p2):
    rolls = list(itertools.product([1, 2, 3], [1, 2, 3], [1, 2, 3]))

    @cache
    def game(p1, p1_score, p2, p2_score, *, p1_turn: bool = True):
        if p1_score >= 21:
            return 1, 0
        if p2_score >= 21:
            return 0, 1

        counts = (0, 0)
        for roll in rolls:
            if p1_turn:
                new_p1 = move(p1, sum(roll))
                new_p1_score = p1_score + score(new_p1)
                new_counts = game(new_p1, new_p1_score, p2, p2_score, p1_turn=False)
            else:
                new_p2 = move(p2, sum(roll))
                new_p2_score = p2_score + score(new_p2)
                new_counts = game(p1, p1_score, new_p2, new_p2_score, p1_turn=True)

            counts = (counts[0] + new_counts[0], counts[1] + new_counts[1])

        return counts

    return game(p1, 0, p2, 0)


class TestDay21:

    def test_roll(self):
        assert list(itertools.islice(deterministic_dice(3, 1, 4), 3)) == [
            [1, 2, 3], [4, 1, 2], [3, 4, 1]
        ]

    def test_part1_sample(self):
        assert part1(p1=4, p2=8) == 739785

    def test_part1(self):
        x = part1(p1=3, p2=7)
        assert x == 1006866

    def test_part2_sample(self):
        assert part2(p1=4, p2=8) == (444356092776315, 341960390180808)

    def test_part2(self):
        assert part2(p1=3, p2=7) == (273042027784929, 188619139770374)
