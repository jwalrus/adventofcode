import itertools as it
import more_itertools as mit
import pytest


class BingoCard:

    def __init__(self, numbers):
        _columns = tuple(c for c in zip(*numbers))
        self.numbers = numbers
        self.candidate_rows = set(numbers).union(set(_columns))

    def __repr__(self):
        return f"BingoCard<{self.numbers}>"

    def score(self, draw, history):
        for row in self.candidate_rows:
            if set(row).difference(history) == set():
                not_drawn = [x for x in it.chain.from_iterable(self.numbers) if x not in history]
                return sum(not_drawn) * draw
        return None


def call_numbers(draws):
    return ((num, set(draws[:i + 1])) for i, num in enumerate(draws))


def part1(puzzle):
    draws, cards = puzzle
    for draw, history in call_numbers(draws):
        for card in cards:
            score = card.score(draw, history)
            if score is not None:
                return score


def part2(puzzle):
    draws, cards = puzzle
    last_round = -1
    last_score = -1
    for card in cards:
        for i, round in enumerate(call_numbers(draws)):
            draw, history = round
            score = card.score(draw, history)
            if score is not None:
                last_round = i if i > last_round else last_round
                last_score = score if i == last_round else last_score
                break
    return last_score


class TestDay03:

    def test_puzzle_input(self, puzzle):
        draws, boards = puzzle
        print(draws)
        for board in boards:
            print(board)

    def test_candidate_rows(self):
        card = ((1, 2, 3),
                (4, 5, 6),
                (7, 8, 9))
        assert set(BingoCard(card).candidate_rows) == {
            (1, 2, 3), (4, 5, 6), (7, 8, 9),
            (1, 4, 7), (2, 5, 8), (3, 6, 9),
        }

    def test_draws(self):
        assert list(call_numbers([1, 2, 3, 4])) == [
            (1, {1}),
            (2, {1, 2}),
            (3, {1, 2, 3}),
            (4, {1, 2, 3, 4})
        ]

    def test_part1_sample(self, sample):
        assert part1(sample) == 4512

    def test_part1(self, puzzle):
        assert part1(puzzle) == 60368

    def test_part2_sample(self, sample):
        assert part2(sample) == 1924

    def test_part2(self, puzzle):
        assert part2(puzzle) == 17435


def parse_input(text):
    draws = [int(c) for c in text[0].strip().split(",")]
    boards = [tuple([int(c) for c in line.strip().replace("  ", " ").split(" ")])
              for line in text[1:] if line != "\n"]
    return draws, [BingoCard(tuple(i)) for i in mit.chunked(boards, 5)]


@pytest.fixture(scope="module")
def puzzle():
    with open("day04.txt") as f:
        return parse_input(f.readlines())


@pytest.fixture(scope="module")
def sample():
    with open("day04_sample.txt") as f:
        return parse_input(f.readlines())
