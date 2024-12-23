import sys
from collections import defaultdict


def main():
    with open(sys.argv[1]) as f:
        pairs = [tuple(sorted(p.split("-"))) for p in f.read().splitlines()]
        pairs = sorted(pairs)
    print("part1:", part1(pairs))
    print("part2:", part2(pairs))


def part1(pairs):
    result = 0
    for i in range(len(pairs) - 1):
        for j in range(i + 1, len(pairs)):
            ai, bi = pairs[i]
            aj, bj = pairs[j]
            if ai == aj and (bi, bj) in pairs:
                if any(v.startswith("t") for v in [ai, bi, bj]):
                    result += 1

    return result


def part2(pairs):
    graph = defaultdict(set)
    for a, b in pairs:
        graph[a].add(b)
        graph[b].add(a)

    maximal_clique = bron_kerbosch(graph)

    return ",".join(maximal_clique)


# https://en.wikipedia.org/wiki/Bron–Kerbosch_algorithm
def bron_kerbosch(graph):
    rs = list()

    def recur(R, P, X):
        if not P and not X:
            rs.append(R)
            return R
        for v in set(P):
            recur(R | {v}, P & graph[v], X & graph[v])
            P = P - {v}
            X = X | {v}

    recur(set(), graph.keys(), set())

    mx = []
    for r in rs:
        if len(r) > len(mx):
            mx = r
    return sorted(mx)


if __name__ == '__main__':
    main()
