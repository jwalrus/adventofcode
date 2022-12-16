import re

import sys
from collections import defaultdict, deque


def parse(lines):
    regex = re.compile(r"^Valve (?P<id>[A-Z]+) has flow rate=(?P<rate>\d+); .+ to (valve|valves) (?P<valves>.+)$")
    matches = [re.match(regex, line) for line in lines]
    scan_output = [
        (match["id"], int(match["rate"]), list(match["valves"].split(", ")))
        for match in matches
    ]

    graph = defaultdict(list)
    for scan in scan_output:
        for _next in scan[2]:
            graph[scan[0]].append(_next)

    rates = {scan[0]: scan[1] for scan in scan_output}

    return graph, rates


def bfs(start, graph):
    queue = deque([(start, 0)])
    visited = {start}
    distances = dict()

    while queue:
        cur, depth = queue.popleft()
        for n in graph[cur]:
            if n not in visited:
                queue.append((n, depth + 1))
                visited.add(n)
                distances[n] = depth + 1

    return distances


def dfs(start, targets, distances, rates, t, seen):
    seen = seen | {start}
    targets = targets - seen
    best_flow = 0

    for target in targets:
        new_t = t - distances[(start, target)] - 1  # plus 1 is opening the valve
        if new_t > 0:
            flow = new_t * rates[target] + dfs(target, targets, distances, rates, new_t, seen)
            if flow > best_flow:
                best_flow = flow

    return best_flow


def part1(graph, rates):
    distances = {(k, n): d for k in graph for n, d in bfs(k, graph).items()}
    targets = {valve for valve, rate in rates.items() if rate > 0}
    return dfs("AA", targets, distances, rates, 30, seen=set())


def main():
    with open(sys.argv[1], "r") as f:
        graph, rates = parse(f.read().split("\n"))
        print("part1:", part1(graph, rates))  # 1796


if __name__ == "__main__":
    main()
