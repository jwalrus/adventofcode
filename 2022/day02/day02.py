R = 0
P = 1
S = 2


def plays(other, me):
    return ord(other) % ord("A"), ord(me) % ord("X")


def part1(other, me):
    return (me - other + 1) % 3 * 3 + (me + 1)


def part2(other, outcome):
    return (outcome + other - 1) % 3 + 1 + outcome * 3


with open("input.txt", "r") as f:
    games = [plays(*line.split(" ")) for line in f.read().split("\n")]
    print("part1:", sum(part1(*game) for game in games))
    print("part2:", sum(part2(*game) for game in games))
