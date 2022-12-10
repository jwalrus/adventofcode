import sys


def cycles(lines):
    register = 1
    for line in lines:
        if line.startswith("noop"):
            yield register
        else:
            n = int(line[5:].strip())
            yield register
            yield register
            register = register + n


def main():
    with open(sys.argv[1], "r") as f:
        lines = f.read().split("\n")
        result = 0
        for i, r in enumerate(cycles(lines)):
            if i in [20, 60, 100, 140, 180, 220]:
                result = result + (i * r)

        print("part1:", result)  # 13140

        screen = ["."] * 240

        for crt, sprite in enumerate(cycles(lines)):
            print(crt, sprite)
            if crt % 40 in {sprite - 1, sprite, sprite + 1}:
                screen[crt] = "#"

        print("part2:")  # PLULKBZH
        for i, pxl in enumerate(screen):
            if i % 40 == 0:
                print("")
            print(pxl, end="")


if __name__ == '__main__':
    main()
