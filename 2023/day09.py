def part1(seqs):
    def go(xs):
        if all(x == 0 for x in xs):
            return 0

        diffs = [y - x for x, y in zip(xs, xs[1:])]
        return xs[-1] + go(diffs)

    return sum(go(seq) for seq in seqs)


def main():
    with open(0) as f:
        lines = f.read().splitlines()
        seqs = [[int(x) for x in line.split()] for line in lines]

    print("A:", part1(seqs))  # 1731106378
    seqs_r = [seq[::-1] for seq in seqs]
    print("B:", part1(seqs_r))  # 1087


if __name__ == '__main__':
    main()
