import itertools
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
    best_order = []

    for target in targets:
        new_t = t - distances[(start, target)] - 1  # plus 1 is opening the valve
        if new_t > 0:
            flow, order = dfs(target, targets, distances, rates, new_t, seen)
            flow = new_t * rates[target] + flow
            order = [target] + order
            if flow > best_flow:
                best_flow = flow
                best_order = order

    return best_flow, best_order


def part1(graph, rates, t):
    distances = {(k, n): d for k in graph for n, d in bfs(k, graph).items()}
    targets = {valve for valve, rate in rates.items() if rate > 0}
    return dfs("AA", targets, distances, rates, t, seen=set())


def part2(graph, rates, t):
    distances = {(k, n): d for k in graph for n, d in bfs(k, graph).items()}
    targets = {valve for valve, rate in rates.items() if rate > 0}
    targets = set(itertools.permutations(targets, 2))

    def dfs2(me, el, targetz, t_me, t_el, seen):
        best_flow_me = 0
        best_flow_el = 0
        best_me = []
        best_el = []

        seen = seen | {me, el}
        targetz = {(x, y) for x, y in targetz if x not in seen and y not in seen}

        for target_me, target_el in targetz:
            new_t_me = t_me - distances[(me, target_me)] - 1
            new_t_el = t_el - distances[(el, target_el)] - 1

            flow_me, flow_el, order_me, order_el = 0, 0, [], []
            match new_t_me > 0, new_t_el > 0:
                case True, True:
                    flow_me, flow_el, order_me, order_el = dfs2(target_me, target_el, targetz, new_t_me, new_t_el, seen)
                    flow_me += new_t_me * rates[target_me]
                    flow_el += new_t_el * rates[target_el]
                    order_me = [target_me] + order_me
                    order_el = [target_el] + order_el
                case True, False:
                    flow_me, order_me = dfs(target_me, {a for a, _ in targetz}, distances, rates, new_t_me, seen)
                    flow_me += new_t_me * rates[target_me]
                    flow_el, order_el = 0, []
                    order_me = [target_me] + order_me
                case False, True:
                    flow_el, order_el = dfs(target_el, {b for _, b in targetz}, distances, rates, new_t_el, seen)
                    flow_el += new_t_el * rates[target_el]
                    flow_me, order_me = 0, []
                    order_el = [target_el] + order_el
                case _:
                    pass

            if flow_me + flow_el > best_flow_el + best_flow_me:
                best_flow_me = flow_me
                best_flow_el = flow_el
                best_me = order_me
                best_el = order_el

        return best_flow_me, best_flow_el, best_me, best_el

    me_f, el_f, me_o, el_o = dfs2("AA", "AA", targets, 26, 26, set())
    return me_f + el_f, me_o, el_o


def main():
    with open(sys.argv[1], "r") as f:
        graph, rates = parse(f.read().split("\n"))
        print("part1:", part1(graph, rates, t=30))  # 1796
        print("part2:", part2(graph, rates, t=26))  # 1999


if __name__ == "__main__":
    main()
