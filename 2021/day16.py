import operator
from functools import reduce
from typing import List

import pytest


def hex_to_bin(h: str) -> str:
    d = {
        "0": "0000", "1": "0001", "2": "0010", "3": "0011",
        "4": "0100", "5": "0101", "6": "0110", "7": "0111",
        "8": "1000", "9": "1001", "A": "1010", "B": "1011",
        "C": "1100", "D": "1101", "E": "1110", "F": "1111",
    }
    return "".join(d[c] for c in h)


def to_int(b: str) -> int:
    return int(b, 2)


def parse_literal(b: str):
    def go(xs: str, acc: List[str]):
        acc.append(xs[1:5])
        if xs.startswith("1"):
            return go(xs[5:], acc)
        else:
            return to_int("".join(acc)), xs[5:]

    version = to_int(b[:3])
    type_ = to_int(b[3:6])
    literal, b = go(b[6:], [])
    return (version, type_, literal), b


def parse_11(b):
    def go(xs: str, num: int, acc: List[str]):
        if num == 0:
            return acc, xs
        else:
            packet, xs = parse(xs)
            acc.append(packet)
            return go(xs, num - 1, acc)

    version = to_int(b[:3])
    type_ = to_int(b[3:6])
    num = to_int(b[7:7 + 11])
    packets, b = go(b[7 + 11:], num, [])
    return (version, type_, packets), b


def parse_15(b):
    def go(xs: str, bits_remaining: int, acc: List[str]):
        n = len(xs)
        if bits_remaining == 0:
            return acc, xs
        else:
            packet, xs = parse(xs)
            acc.append(packet)
            return go(xs, bits_remaining - (n - len(xs)), acc)

    version = to_int(b[:3])
    type_ = to_int(b[3:6])
    num = to_int(b[7:7 + 15])
    packets, b = go(b[7 + 15:], num, [])
    return (version, type_, packets), b


def parse_operator(b):
    match b[6]:
        case "0":
            return parse_15(b)
        case "1":
            return parse_11(b)


def parse(b: str):
    match to_int(b[3:6]):
        case 4:
            return parse_literal(b)
        case _:
            return parse_operator(b)


def sum_versions(packet):
    if isinstance(packet[2], list):
        return packet[0] + sum(sum_versions(p) for p in packet[2])
    else:
        return packet[0]


def part1(puzzle):
    packet, _ = parse(puzzle)
    return sum_versions(packet)


def score(packet):
    _, type_, packets = packet
    match type_:
        case 4:
            return packets
        case 0:
            return reduce(operator.add, [score(p) for p in packets])
        case 1:
            return reduce(operator.mul, [score(p) for p in packets])
        case 2:
            return min([score(p) for p in packets])
        case 3:
            return max([score(p) for p in packets])
        case 5:
            return 1 if score(packets[0]) > score(packets[1]) else 0
        case 6:
            return 1 if score(packets[0]) < score(packets[1]) else 0
        case 7:
            return 1 if score(packets[0]) == score(packets[1]) else 0


def part2(puzzle):
    packet, _ = parse(puzzle)
    return score(packet)


class TestDay16:

    def test_puzzle_input(self, puzzle):
        assert set(puzzle) == {"0", "1"}

    def test_hex_to_bin(self):
        assert hex_to_bin("D2FE28") == "110100101111111000101000"
        assert hex_to_bin("38006F45291200") == "00111000000000000110111101000101001010010001001000000000"
        assert hex_to_bin("EE00D40C823060") == "11101110000000001101010000001100100000100011000001100000"

    def test_parse_literal(self):
        (version, type_, literal), b = parse_literal("110100101111111000101000")
        assert version == 6
        assert type_ == 4
        assert literal == 2021
        assert b == "000"

    def test_parse_op15(self):
        b = "00111000000000000110111101000101001010010001001000000000"
        (version, type_, packet), b = parse(b)
        assert version == 1
        assert type_ == 6
        assert packet == [(6, 4, 10), (2, 4, 20)]
        assert b == "0000000"

    def test_parse_op11(self):
        b = "11101110000000001101010000001100100000100011000001100000"
        (version, type_, packet), b = parse(b)
        assert version == 7
        assert type_ == 3
        assert packet == [(2, 4, 1), (4, 4, 2), (1, 4, 3)]
        assert b == "00000"

    def test_part1_sample(self):
        assert part1(hex_to_bin("8A004A801A8002F478")) == 16

    def test_part1(self, puzzle):
        assert part1(puzzle) == 854

    def test_part2(self, puzzle):
        assert part2(puzzle) == 186189840660


def parse_input(text):
    return hex_to_bin(text.strip())


@pytest.fixture(scope="module")
def puzzle():
    with open("day16.txt") as f:
        return parse_input(f.read())


@pytest.fixture(scope="module")
def sample():
    from textwrap import dedent
    return parse_input(dedent("""\

    """))
