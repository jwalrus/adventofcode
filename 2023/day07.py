from collections import Counter

FIVE_OF_KIND = 0
FOUR_OF_KIND = 1
FULL_HOUSE = 2
THREE_OF_KIND = 3
TWO_PAIR = 4
ONE_PAIR = 5
HIGH_CARD = 6


def classify(hand):
    counts = Counter(hand)
    if len(counts) == 1:
        return FIVE_OF_KIND

    (_, na), (_, nb) = counts.most_common(2)
    match (na, nb):
        case (4, 1):
            return FOUR_OF_KIND
        case (3, 2):
            return FULL_HOUSE
        case (3, 1):
            return THREE_OF_KIND
        case (2, 2):
            return TWO_PAIR
        case (2, 1):
            return ONE_PAIR
        case _:
            return HIGH_CARD


def replace_j(hand, new_c, *, j_num=12) -> list[tuple]:
    results = []
    for i, c in enumerate(hand):
        if c == j_num:
            new = list(hand)
            new[i] = new_c
            results.append(tuple(new))
    return results


def best_hand(hand):
    def go(classification, nums: tuple, nj: int):

        if nj < 1:
            return classification, nums

        best_classification = classification
        bh = nums

        for i, c in enumerate(hand):
            if c == 12:
                continue
            else:
                for new_hand in replace_j(nums, c):
                    test_class, test_hand = go(classify(new_hand), new_hand, nj - 1)
                    best_classification, bh = min((best_classification, bh), (test_class, test_hand))

        return best_classification, bh

    nj = sum(1 for x in hand if x == 12)
    return go(classify(hand), hand, nj)[0]


def part1(lines, ranking):
    hand_bets = {tuple([ranking[c] for c in x[0]]): int(x[1]) for line in lines if (x := line.split())}
    hand_rankings = sorted([(classify(hand), hand) for hand in hand_bets])
    wins = [hand_bets[hand] for _, hand in hand_rankings[::-1]]
    return sum((i + 1) * bet for i, bet in enumerate(wins))


def convert2(hand, ranking):
    return tuple([ranking[c] for c in hand])


def part2(lines, ranking):
    hand_bets = {convert2(x[0], ranking): int(x[1]) for line in lines if (x := line.split())}
    hand_rankings = sorted([(best_hand(hand), hand) for hand in hand_bets])
    wins = [hand_bets[hand] for _, hand in hand_rankings[::-1]]
    return sum((i + 1) * bet for i, bet in enumerate(wins))


def main():
    with open(0) as f:
        lines = f.read().splitlines()
    ranks_a = {k: i for i, k in enumerate("AKQJT98765432")}
    print("A:", part1(lines, ranks_a))  # 249,390,788
    ranks_b = {k: i for i, k in enumerate("AKQT98765432J")}
    print("B:", part2(lines, ranks_b))  # 248,750,248


if __name__ == "__main__":
    main()
