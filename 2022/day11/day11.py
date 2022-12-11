import math
import sys
from functools import reduce
from typing import Callable, List, NamedTuple


class Monkey(NamedTuple):
    id: int
    items: List[int]
    operation: Callable[[int], int]
    test: Callable[[int], int]
    inspected: List[int]
    mod: int

    def catch(self, item):
        self.items.append(item)

    def inspect(self, item):
        self.inspected.append(item)
        return self.operation(item)

    @classmethod
    def make(cls, raw):
        rows = raw.split("\n")
        _, _id = rows[0].split(" ")
        _, items = rows[1].split(": ")
        _, op = rows[2].split(" = ")
        _, mod = rows[3].split(" by ")
        _, on_true = rows[4].split(" to monkey ")
        _, on_false = rows[5].split(" to monkey ")

        mod = int(mod.strip())
        on_true = int(on_true.strip())
        on_false = int(on_false.strip())

        return Monkey(
            id=int(_id.strip(" :")),
            items=[int(i) for i in items.split(", ")],
            operation=lambda old: eval(op.strip()),
            test=lambda old: on_true if old % mod == 0 else on_false,
            inspected=[],
            mod=mod,
        )


def monkey_business(monkeys, rounds, xanax, verbose=False):
    monkey_map = {m.id: m for m in monkeys}

    for r in range(rounds):

        for i in range(len(monkey_map)):
            monkey = monkey_map[i]

            while monkey.items:
                item = monkey.items.pop()
                worry = xanax(monkey.inspect(item))
                _next = monkey_map[monkey.test(worry)]
                _next.catch(worry)

        if verbose and (r + 1) in [1, 10, 20, 1000, 2000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]:
            print(f"== After round {r + 1} ==")
            for m in monkeys:
                print(f"Monkey {m.id} inspected items {len(m.inspected)} times.")
            print()

    counts = sorted(len(m.inspected) for m in monkeys)

    return counts[-1] * counts[-2]


def main():
    with open(sys.argv[1], "r") as f:
        monkeys = [Monkey.make(m) for m in f.read().split("\n\n")]

    print("part1:", monkey_business(monkeys, 20, lambda x: x // 3, verbose=False))  # 100345

    with open(sys.argv[1], "r") as f:
        monkeys = [Monkey.make(m) for m in f.read().split("\n\n")]

    # limit worry
    lcm = reduce(math.lcm, [m.mod for m in monkeys], 1)
    print("part2:", monkey_business(monkeys, 10_000, lambda x: x % lcm, verbose=False))  # 28537348205


if __name__ == "__main__":
    main()
