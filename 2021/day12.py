import itertools as it

import pytest


def neighbors(v, edges):
    edges = [edge for edge in edges if v in edge]
    return set(n for n in it.chain.from_iterable(edges) if n != v)


def graphify(edges):
    return {v: neighbors(v, edges) for v in (set(it.chain.from_iterable(edges)))}


def small_cave(v):
    return v == v.lower()


def update_visited(v, visited):
    if small_cave(v):
        new = dict(visited)
        new[v] = new.get(v, 0) + 1
        return new
    else:
        return visited


def traverse(graph, start, visitable):
    def recur(v, visited):
        if v == "end":
            return 1
        else:
            visited = update_visited(v, visited)
            return sum([recur(x, visited) for x in graph[v] if visitable(x, visited)])

    return recur(start, {})


def part1(puzzle):
    def visitable(v, visited):
        return v not in visited

    return traverse(graphify(puzzle), "start", visitable)


def part2(puzzle):
    def visitable(v, visited):
        match visited.get(v, 0):
            case 0:
                return True
            case 1:
                return all(v < 2 for v in visited.values()) and v not in ("start", "end")
            case _:
                return False

    return traverse(graphify(puzzle), "start", visitable)


class TestDay12:

    def test_puzzle_input(self, sample, puzzle):
        assert len(sample) == 7
        assert len(puzzle) == 24

    def test_graphify(self):
        assert graphify([("a", "b"), ("b", "c")]) == {"a": {"b"}, "b": {"a", "c"}, "c": {"b"}}

    def test_part1_sample(self, sample):
        assert part1(sample) == 10

    def test_part1(self, puzzle):
        assert part1(puzzle) == 4411

    def test_part2_sample(self, sample):
        assert part2(sample) == 36

    def test_part2(self, puzzle):
        assert part2(puzzle) == 136767


def parse_input(text):
    return [tuple(line.strip().split("-")) for line in text.split("\n") if line.strip() != ""]


@pytest.fixture(scope="module")
def puzzle():
    with open("day12.txt") as f:
        return parse_input(f.read())


@pytest.fixture(scope="module")
def sample():
    return parse_input("""start-A
    start-b
    A-c
    A-b
    b-d
    A-end
    b-end
    """)
