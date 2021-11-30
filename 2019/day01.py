def load():
    with open("day01.txt") as f:
        xs = f.readlines()
        return [int(x) for x in xs]


def part1(xs):
    return sum([x // 3 - 2 for x in xs])


def part2(xs):

    def go(x, acc):
        if x == 0:
            return acc
        else:
            y = x // 3 - 2
            z = y if y > 0 else 0
            acc.append(z)
            return go(z, acc)

    return sum([sum(go(x, [])) for x in xs])


class TestFoo:

    def test_part1(self):
        assert part1(load()) == 3087896

    def test_part2(self):
        assert part2(load()) == 4628989
