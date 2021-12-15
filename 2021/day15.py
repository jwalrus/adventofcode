import heapq
from collections import defaultdict
from typing import Dict, List, Tuple

import pytest

Vertex = Tuple[int, int]
Graph = Dict[Vertex, int]


def make_graph(xs: List[List[int]]) -> Graph:
    return {(i, j): x for i, row in enumerate(xs) for j, x in enumerate(row)}


def neighbors(v: Vertex, graph: Graph) -> List[Vertex]:
    x, y = v
    ns = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
    return [n for n in ns if graph.get(n) is not None]


def expand_graph(graph: Graph, m, n: int = 5) -> Graph:
    expanded = {}

    for i in range(n):
        for j in range(n):
            for k, v in graph.items():
                x, y = k
                new_v = (v + i + j)
                new_v = new_v if new_v <= 9 else (new_v % 10) + 1
                expanded[(m * i + x, m * j + y)] = new_v

    return expanded


def dijkstra(g: Graph, start: Vertex):
    inf = 9999999999999
    distances = defaultdict(lambda: inf)
    previous = {}
    pq = [(0, start)]
    heapq.heapify(pq)

    while pq:
        cur, u = heapq.heappop(pq)

        for v in neighbors(u, g):
            dist = cur + g.get(v, inf)
            if dist < distances[v]:
                distances[v] = dist
                previous[v] = u
                heapq.heappush(pq, (dist, v))

    return distances, previous


def part1(puzzle):
    n = len(puzzle)
    graph = make_graph(puzzle)
    distances, path = dijkstra(graph, (0, 0))
    return distances[(n - 1, n - 1)]


def part2(puzzle):
    n = len(puzzle) * 5
    graph = expand_graph(make_graph(puzzle), len(puzzle), n=5)
    distances, path = dijkstra(graph, (0, 0))
    return distances[(n - 1, n - 1)]


class TestDay15:

    def test_puzzle_input(self, sample, puzzle):
        assert len(sample[0]) == 10
        assert len(sample) == 10
        assert len(puzzle[0]) == 100
        assert len(puzzle) == 100

    def test_part1_sample(self, sample):
        assert part1(sample) == 40

    def test_part1(self, puzzle):
        assert part1(puzzle) == 423

    def test_expand(self):
        assert expand_graph({(0, 0): 8}, 1, n=3) == {
            (0, 0): 8, (0, 1): 9, (0, 2): 1,
            (1, 0): 9, (1, 1): 1, (1, 2): 2,
            (2, 0): 1, (2, 1): 2, (2, 2): 3
        }

    def test_expand_2(self):
        g = {
            (0, 0): 1, (0, 1): 1,
            (1, 0): 1, (1, 1): 1
        }

        assert expand_graph(g, 2, n=3) == {
            (0, 0): 1, (0, 1): 1, (0, 2): 2, (0, 3): 2, (0, 4): 3, (0, 5): 3,
            (1, 0): 1, (1, 1): 1, (1, 2): 2, (1, 3): 2, (1, 4): 3, (1, 5): 3,

            (2, 0): 2, (2, 1): 2, (2, 2): 3, (2, 3): 3, (2, 4): 4, (2, 5): 4,
            (3, 0): 2, (3, 1): 2, (3, 2): 3, (3, 3): 3, (3, 4): 4, (3, 5): 4,

            (4, 0): 3, (4, 1): 3, (4, 2): 4, (4, 3): 4, (4, 4): 5, (4, 5): 5,
            (5, 0): 3, (5, 1): 3, (5, 2): 4, (5, 3): 4, (5, 4): 5, (5, 5): 5,

        }

    def test_part2_sample(self, sample):
        assert part2(sample) == 315

    def test_part2(self, puzzle):
        assert part2(puzzle) == 2778


def parse_input(text):
    lines = [list(line.strip()) for line in text.split("\n") if line != ""]
    return [[int(x) for x in line] for line in lines]


@pytest.fixture(scope="module")
def puzzle():
    with open("day15.txt") as f:
        return parse_input(f.read())


@pytest.fixture(scope="module")
def sample():
    from textwrap import dedent
    return parse_input(dedent("""\
        1163751742
        1381373672
        2136511328
        3694931569
        7463417111
        1319128137
        1359912421
        3125421639
        1293138521
        2311944581
    """))
