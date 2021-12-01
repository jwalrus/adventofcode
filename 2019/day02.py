import itertools

import pytest


def load():
    with open("day02.txt") as f:
        return [int(x) for x in f.readline().split(',')]


def execute(program):
    result = list(program)
    i = 0
    while i < len(program):
        if result[i] == 99:
            break
        elif result[i] == 1:
            result[result[i+3]] = result[result[i+1]] + result[result[i+2]]
        else:
            result[result[i + 3]] = result[result[i + 1]] * result[result[i + 2]]
        i = i + 4
    return result


def part1(puzzle, noun=12, verb=2):
    puzzle[1] = noun
    puzzle[2] = verb
    result = execute(puzzle)
    return result[0]


def part2(puzzle, target=19690720):
    for noun, verb in itertools.combinations(range(0, 100), 2):
        if part1(list(puzzle), noun=noun, verb=verb) == target:
            return noun, verb




@pytest.mark.parametrize('initial,final', [
    ([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]),
    ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
    ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
    ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
    ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
])
def test_examples(initial, final):
    assert execute(initial) == final


def test_part1():
    assert part1(load()) == 4570637


def test_part2():
    assert part2(load()) == (54, 85)
