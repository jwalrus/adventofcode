import operator as op
import sys
from collections import deque
from typing import Callable, NamedTuple


class Speak(NamedTuple):
    name: str
    number: int


class Wait(NamedTuple):
    name: str
    left: str
    op: Callable[[int, int], int]
    right: str


def parse(line):
    xs = line.replace(":", "").split(" ")
    if len(xs) == 2:
        return Speak(xs[0], int(xs[1]))
    else:
        match xs[2]:
            case "+":
                f = op.add
            case "-":
                f = op.sub
            case "*":
                f = op.mul
            case "/":
                f = op.truediv
            case _:
                raise ValueError(f"unexpected value {xs[2]}")
        return Wait(xs[0], xs[1], f, xs[3])


def part1(monkeys):
    spoken = dict()
    queue = deque(monkeys)

    while queue:
        monkey = queue.popleft()
        if isinstance(monkey, Speak):
            spoken[monkey.name] = monkey.number
        else:
            left = spoken.get(monkey.left)
            rght = spoken.get(monkey.right)
            if left is None or rght is None:
                queue.append(monkey)
            else:
                spoken[monkey.name] = monkey.op(left, rght)

        if spoken.get("root") is not None:
            return spoken["root"]

    raise ValueError("failed to find root")


def part2(monkeys):
    queue0 = deque(monkeys)

    li, ri = 0, 100_000_000_000_000_000_000
    while li < ri:
        mi = (ri + li) // 2
        for _ in monkeys:
            monkey = queue0.popleft()
            if monkey.name == "humn":
                monkey = monkey._replace(number=mi)
            if monkey.name == "root":
                monkey = monkey._replace(op=op.sub)
            queue0.append(monkey)

        result = part1(queue0)
        if result == 0:
            return mi
        elif result < 0:
            li, ri = li, mi
        else:
            li, ri = mi, ri

    raise ValueError("nope :(")


def main():
    with open(sys.argv[1], "r") as f:
        monkeys = [parse(line) for line in f.read().split("\n")]
        print("part1:", part1(monkeys))  # 268597611536314
        print("part2:", part2(monkeys))  # 3451534022348


if __name__ == "__main__":
    main()
