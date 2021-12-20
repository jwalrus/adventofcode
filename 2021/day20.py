import functools
from functools import cache

import more_itertools as mit
import pytest


@cache
def neighbors(p):
    row, col = p
    # @formatter:off
    return [
        (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
        (row,     col - 1), (row,     col), (row,     col + 1),
        (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)
    ]
    # @formatter:on


def lookup_val(ns, image, min_row, min_col, max_row, max_col, outside):
    idx = 0
    for r, c in ns:
        idx <<= 1
        idx |= ((r, c) in image)
        idx |= outside and (r < min_row or r > max_row or c < min_col or c > max_col)
    return idx


def enhance(image, enhancer, outside):
    (min_row, _), (max_row, _) = mit.minmax(image, key=lambda p: p[0])
    (_, min_col), (_, max_col) = mit.minmax(image, key=lambda p: p[1])
    # create new image

    new_image = set()
    for row in range(min_row - 10, max_row + 20):
        for col in range(min_col - 10, max_row + 20):
            pixel = (row, col)
            ns = neighbors(pixel)
            idx = lookup_val(ns, image, min_row, min_col, max_row, max_col, outside)
            if enhancer[idx] == "#":
                new_image.add(pixel)

    return new_image


def print_image(image):
    (min_row, _), (max_row, _) = mit.minmax(image, key=lambda p: p[0])
    (_, min_col), (_, max_col) = mit.minmax(image, key=lambda p: p[1])
    for row in range(min_row - 1, max_row + 2):
        print()
        for col in range(min_col - 1, max_col + 2):
            val = "#" if (row, col) in image else "."
            print(val, end="")
    print()


def part1(puzzle, *, n=2):
    enhancer, image0 = puzzle
    image_n = functools.reduce(
        lambda img, n: enhance(img, enhancer, enhancer[0] == "#" and n % 2 == 1),
        range(n),
        image0
    )
    return len(image_n)


def part2(puzzle):
    return part1(puzzle, n=50)


class TestDay20:

    def test_part1_sample(self, sample):
        assert part1(sample) == 35

    def test_part1(self, puzzle):
        x = part1(puzzle)
        assert x == 5479

    def test_part2_sample(self, sample):
        assert part2(sample) == 3351

    def test_part2(self, puzzle):
        assert part2(puzzle) == 0


def parse_input(text):
    enhancer, image = [x.strip() for x in text.split("\n\n") if x != ""]
    image = [x.strip() for x in image.split("\n") if x != ""]

    d = {(row, col)
         for row, vals in enumerate(image)
         for col, val in enumerate(vals)
         if val == "#"}

    return enhancer, d


@pytest.fixture(scope="module")
def puzzle():
    with open("day20.txt") as f:
        return parse_input(f.read())


@pytest.fixture(scope="module")
def sample():
    from textwrap import dedent
    return parse_input(dedent("""\
        ..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#
        
        #..#.
        #....
        ##..#
        ..#..
        ..###
    """))
