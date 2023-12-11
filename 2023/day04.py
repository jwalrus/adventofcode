import re
import sys


def num_winners(winners, numbers) -> int:
    winners = {int(m.group()) for m in re.finditer(r"\d+", winners)}
    numbers = {int(m.group()) for m in re.finditer(r"\d+", numbers)}
    intersection = winners.intersection(numbers)
    return len(intersection)


def points(winners, numbers) -> int:
    n = num_winners(winners, numbers)
    return 2 ** (n - 1) if n > 0 else 0


def part1(xs):
    xs = [re.sub(r"Card\s+\d+: ", "", x).split(" | ") for x in xs]
    return sum(points(winners, numbers) for (winners, numbers) in xs)


def part2(xs):
    xs = {
        int(re.match(r"Card\s+(\d+): ", x).group(1)): re.sub(r"Card\s+(\d+): ", "", x).split(" | ")
        for x in xs
    }

    base_prizes = {
        card: num_winners(winners, numbers)
        for card, (winners, numbers) in xs.items()
    }

    prizes = {card: 1 for card in base_prizes}
    for card, n in base_prizes.items():

        for i in range(n):
            ix = card + i + 1
            if prizes.get(ix):
                prizes[ix] += prizes[card]

    return sum(prizes.values())


if __name__ == "__main__":
    lines = sys.stdin.read().splitlines()

    print("A:", part1(lines))  # 21,558
    print("B:", part2(lines))  # 10,425,665