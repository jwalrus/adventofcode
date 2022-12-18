import sys

with open(sys.argv[1], "r") as f:
    elves = sorted([sum(int(x) for x in line.splitlines()) for line in f.read().split("\n\n")], reverse=True)
    print("part1:", elves[0])  # 69795
    print("part2:", sum(elves[:3]))  # 208437
