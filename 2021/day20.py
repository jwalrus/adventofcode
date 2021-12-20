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


def lookup_val(ns, image):
    vals = ["1" if n in image else "0" for n in ns]
    return int("".join(vals), 2)


def enhance_pixel(pixel, image, enhancer):
    ns = neighbors(pixel)
    enhancement_val = lookup_val(ns, image)
    return enhancer[enhancement_val]


def enhance(image, enhancer):
    image_set = {n for pixel in image for n in neighbors(pixel)}
    return {pixel for pixel in image_set
            if enhance_pixel(pixel, image, enhancer) == "1"}


def print_image(image):
    (min_row, _), (max_row, _) = mit.minmax(image, key=lambda p: p[0])
    (_, min_col), (_, max_col) = mit.minmax(image, key=lambda p: p[1])
    for row in range(min_row - 1, max_row + 2):
        print()
        for col in range(min_col - 1, max_col + 2):
            val = "#" if (row, col) in image else "."
            print(val, end="")
    print()


def part1(puzzle):
    enhancer, image0 = puzzle
    print("\n\nIMAGE 0")
    print_image(image0)
    image1 = enhance(image0, enhancer)
    print("\n\nIMAGE 1")
    print_image(image1)
    print("\n\nIMAGE 2")
    image2 = enhance(image1, enhancer)
    print_image(image2)
    return len(image2)


def part2(puzzle):
    return -1


class TestDay20:

    def test_part1_sample(self, sample):
        assert part1(sample) == 35

    def test_part1(self, puzzle):
        x = part1(puzzle)
        assert x == 0

    def test_part2_sample(self, sample):
        assert part2(sample) == 0

    def test_part2(self, puzzle):
        assert part2(puzzle) == 0


def parse_input(text):
    enhancer, image = [x.strip() for x in text.split("\n\n") if x != ""]
    enhancer = ["1" if x == "#" else "0" for x in enhancer]
    image = [x.strip() for x in image.split("\n") if x != ""]
    image = [["1" if x == "#" else "0" for x in row] for row in image]

    d = {(row, col)
         for row, vals in enumerate(image)
         for col, val in enumerate(vals)
         if val == "1"}

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
