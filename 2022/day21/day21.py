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
            return int(spoken["root"])

    return 0


def main():
    with open(sys.argv[1], "r") as f:
        monkeys = [parse(line) for line in f.read().split("\n")]
        print("part1:", part1(monkeys))  # 268597611536314


if __name__ == "__main__":
    main()
