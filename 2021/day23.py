from functools import cache
from typing import Set

import pytest

Position = tuple
INF = 999999999999999


def goal_met(board) -> bool:
    return all(at_goal(board, p) for p in board)


def piece_at(board, position):
    for k, v in board.items():
        if v == position:
            return k
    return None


def can_leave_initial_room(board, piece) -> bool:
    match board[piece]:
        case (2, col):
            return piece_at(board, (1, col)) is None
        case (1, col):
            return piece_at(board, (0, col - 1)) is None or piece_at(board, (
                0, (col + 1))) is None
        case _:
            return True


@cache
def is_eligible(position, piece):
    match position:
        case (_, 2):
            return piece.startswith("A")
        case (_, 4):
            return piece.startswith("B")
        case (_, 6):
            return piece.startswith("C")
        case (_, 8):
            return piece.startswith("D")
        case _:
            return True


@cache
def goal_col(piece):
    if piece.startswith("A"): return 2
    if piece.startswith("B"): return 4
    if piece.startswith("C"): return 6
    if piece.startswith("D"): return 8
    raise ValueError(f"unknown. {piece=}")


def at_goal(board, piece):
    row, col = board[piece]
    goal = goal_col(piece)
    if col != goal:
        return False
    else:
        match row:
            case 1:
                return piece_at(board, (2, goal)) is None or piece_at(board, (
                    2, goal)).startswith(piece[0])
            case 2:
                return piece_at(board, (1, goal)) is None or piece_at(board, (
                    1, goal)).startswith(piece[0])


def goal_moves(board, piece, *, goal) -> Set[Position]:
    a, b = piece_at(board, (1, goal)), piece_at(board, (2, goal))
    if a is None and b is None:
        return {(2, goal)}
    if a is None and piece[0] == b[0]:
        return {(1, goal)}
    else:
        return set()


def available_moves(b, p) -> Set[Position]:
    def all_moves(board, piece) -> Set[Position]:
        if not can_leave_initial_room(board, piece):
            return set()

        if at_goal(board, piece):
            return set()

        result = set()
        _, col = board[piece]

        for x in range(col + 1, 10 + 1):
            if is_eligible((0, x), piece):
                if (0, x) not in board.values():
                    result.add((0, x))
                else:
                    break

        for x in range(col - 1, -1, -1):
            if is_eligible((0, x), piece):
                if (0, x) not in board.values():
                    result.add((0, x))
                else:
                    break

        return result

    moves = all_moves(b, p)
    row, col = b[p]
    goal = goal_col(p)

    if (0, goal) in moves:
        gm = goal_moves(b, p, goal=goal)
        if gm != set():
            return gm

    if row == 0:
        return set()
    else:
        return moves


def cost(piece, a, b):
    row_a, col_a = a
    row_b, col_b = b
    distance = abs(row_a - 0) + abs(col_a - col_b) + abs(row_b - 0)
    if piece.startswith("A"): return distance * 1
    if piece.startswith("B"): return distance * 10
    if piece.startswith("C"): return distance * 100
    if piece.startswith("D"): return distance * 1000


def all_possible_moves(board):
    moves = set()
    for piece, _ in board.items():
        new_moves = {(piece, move) for move in available_moves(board, piece)}
        moves = moves.union(new_moves)
    return moves


def freeze(d):
    return frozenset((k, v) for k, v in d.items())


def unfreeze(st):
    return {k: v for k, v in st}


@cache
def part1(puzzle, *, current_score=0, best_score=INF):
    puzzle = unfreeze(puzzle)
    if goal_met(puzzle):
        return best_score if best_score < current_score else current_score

    if current_score > best_score:
        return best_score

    for piece, dest in all_possible_moves(puzzle):
        new_puzzle = dict(puzzle)
        new_puzzle[piece] = dest
        tmp = current_score + cost(piece, puzzle[piece], dest)
        new_puzzle = freeze(new_puzzle)
        best_score = part1(
            new_puzzle,
            current_score=tmp,
            best_score=best_score
        )

    return best_score


def part2(puzzle):
    return -1


class TestDay23:

    def test_piece_at(self):
        board = {"A1": (0, 1), "A2": (0, 2)}
        assert piece_at(board, (0, 2)) == "A2"

    def test_can_leave_initial_room(self):
        board = {"B1": (2, 2), "A1": (1, 4), "A2": (2, 4)}
        assert can_leave_initial_room(board, "B1") is True
        assert can_leave_initial_room(board, "A1") is True
        assert can_leave_initial_room(board, "A2") is False

    def test_available_moves(self):
        board = {"A1": (1, 6)}
        assert available_moves(board, "A1") == {(2, 2)}

        board = {"A1": (1, 6), "B1": (2, 2)}
        assert available_moves(board, "A1") == {
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 5), (0, 7), (0, 9), (0, 10)
        }

        board = {"A1": (1, 6), "C2": (2, 6)}
        assert available_moves(board, "C2") == set()

    def test_all_possible_moves(self):
        board = {"A1": (1, 6), "B1": (2, 2)}
        assert all_possible_moves(board) == {
            ("A1", (0, 0)), ("A1", (0, 1)),
            ("A1", (0, 2)), ("A1", (0, 3)),
            ("A1", (0, 5)), ("A1", (0, 7)),
            ("A1", (0, 9)), ("A1", (0, 10)),
            ("B1", (2, 4))
        }

        board = {"B1": (1, 2), "C1": (0, 0), "C2": (0, 1), "A1": (0, 3)}
        assert all_possible_moves(board) == set()

        board = {"D1": (0, 7), "A1": (1, 8)}
        assert all_possible_moves(board) == {('A1', (0, 9)), ('A1', (0, 10))}

    def test_part1_sample(self, sample):
        assert part1(freeze(sample)) == 12521

    def test_part1(self, puzzle):
        assert part1(freeze(puzzle)) == 0

    def test_part2_sample(self, sample):
        assert part2(sample) == 0

    def test_part2(self, puzzle):
        assert part2(puzzle) == 0


def parse_input(text):
    lines = [list(line.strip()) for line in text.split("\n") if line != ""]
    return [[int(x) for x in line] for line in lines]


@pytest.fixture(scope="module")
def puzzle():
    """
                 1
       01234567890
      #############
    0 #...........#
    1 ###C#C#B#D###
    2   #D#A#B#A#
        #########
    """
    return {
        "A1": (2, 8),
        "A2": (2, 4),
        "B1": (1, 6),
        "B2": (2, 6),
        "C1": (1, 2),
        "C2": (1, 4),
        "D1": (2, 2),
        "D2": (1, 8),
    }


@pytest.fixture(scope="module")
def sample():
    """
                 1
       01234567890
      #############
    0 #...........#
    1 ###B#C#B#D###
    2   #A#D#C#A#
        #########
    """
    return {
        "A1": (2, 2),
        "A2": (2, 8),
        "B1": (1, 2),
        "B2": (1, 6),
        "C1": (1, 4),
        "C2": (2, 6),
        "D1": (2, 4),
        "D2": (1, 8),
    }
