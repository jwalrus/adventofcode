def main(xs, pos=50):
    part1, part2 = 0, 0

    for x in xs:
        move = int(x[1:])
        if x.startswith("R"):
            part2 += (pos + move) // 100
            pos = (pos + move) % 100
        else:
            part2 += (((100 - pos) % 100) + move) // 100
            pos = (pos - move) % 100

        part1 += (pos == 0)

    return part1, part2


if __name__ == "__main__":
    import sys

    with open(sys.argv[1], "r") as fh:
        arr = [l.strip() for l in fh.readlines()]
    a, b = main(arr)
    print("part1", a)
    print("part2", b)
