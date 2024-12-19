import sys
from functools import cache


def main():
    with open(sys.argv[1]) as fh:
        patterns, designs = fh.read().split("\n\n")
        patterns = patterns.split(", ")
        designs = designs.split("\n")

    results = run(patterns, designs)
    print("part1:", sum(1 for r in results if r > 0))
    print("part2:", sum(r for r in results))


def run(patterns, designs):
    @cache
    def dfs(design):
        if design == "":
            return 1
        count = 0
        for pattern in patterns:
            if design.startswith(pattern):
                count += dfs(design.removeprefix(pattern))
        return count

    return [dfs(d) for d in designs]


if __name__ == "__main__":
    main()
