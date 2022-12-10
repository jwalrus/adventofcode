import sys
from collections import defaultdict


def part1(lines):
    lines.append("$ cd ..")
    sizes = defaultdict(lambda: 0)
    stack = []

    for line in lines:

        if line.startswith("$ cd "):
            cd = line[5:]
            if cd == "..":
                stack.pop()
            else:
                stack.append(cd)

        elif line.startswith("dir") or line.startswith("$ ls"):
            pass

        else:
            sz, _ = line.split(" ")
            n = int(sz)
            for i, p in enumerate(stack):
                sizes["/".join(stack[:i + 1])] += n

    return sizes


def part2(sizes):
    target = sizes["/"] - (70000000 - 30000000)
    candidates = [v for k, v in sizes.items() if v > target]
    return min(candidates)


def main():
    with open(sys.argv[1], "r") as f:
        lines = f.read().splitlines()
        sizes = part1(lines)
        print("part1:", sum(v for v in sizes.values() if v < 100000))  # 1454188
        print("part2:", part2(sizes))  # 4183246


if __name__ == '__main__':
    main()
