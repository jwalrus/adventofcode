import re
import sys

from typing import NamedTuple


class Inventory(NamedTuple):
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0
    robot_ore: int = 1
    robot_clay: int = 0
    robot_obsidian: int = 0
    robot_geode: int = 0


class Cost(NamedTuple):
    ore: int
    clay: int = 0
    obsidian: int = 0


class Blueprint(NamedTuple):
    id: int
    ore: Cost
    clay: Cost
    obsidian: Cost
    geode: Cost

    @classmethod
    def make(cls, *args):
        args = list(map(int, args))
        return Blueprint(
            id=args[0],
            ore=Cost(ore=args[1]),
            clay=Cost(ore=args[2]),
            obsidian=Cost(ore=args[3], clay=args[4]),
            geode=Cost(ore=args[5], obsidian=args[6])
        )


def search(bp: Blueprint, n: int, verbose=False):
    def build_options(i: Inventory):
        options = []

        for j, robot in enumerate([bp.geode, bp.obsidian, bp.clay, bp.ore]):
            ore, clay, obs = robot
            tmp = [0, 0, 0, 0]
            if i.ore >= ore and i.clay >= clay and i.obsidian >= obs:
                tmp[j] = 1
                options.append(tuple(tmp))

        options.append((0, 0, 0, 0))  # can always do nothing ... but building should be preferred?
        return options

    def dfs(t, inventory, best_result):

        if verbose:
            print(n, t, inventory, best_result)

        # prune bad branches
        max_ore = max(bp.ore.ore, bp.clay.ore, bp.geode.ore, bp.obsidian.ore)
        # if max_ore * (n - t) < inventory.ore:
        #     print("TOO MUCH ORE!")
        #     return inventory
        #
        # if inventory.robot_ore >= max_ore:
        #     if verbose:
        #         print("TOO MANY ORE ROBOTS")
        #     return inventory
        #
        # max_clay = max(bp.ore.clay, bp.clay.clay, bp.geode.clay, bp.obsidian.clay)
        # if max_clay * (n - t) < inventory.clay:
        #     print("TOO MUCH CLAY!")
        #     return inventory
        #
        # if inventory.robot_clay >= max_clay:
        #     if verbose:
        #         print("TOO MANY CLAY ROBOTS")
        #     return inventory

        if (inventory.geode + inventory.robot_geode + (n - t + 1) * (n - t) // 2) < best_result.geode:
            if verbose:
                print("pruning branch!")
            return inventory

        if t > n:
            return inventory

        # branch
        for option in build_options(inventory):
            geo, obs, clay, ore = option
            candidate = inventory._replace(
                ore=inventory.ore + inventory.robot_ore - bp.ore.ore * ore - bp.clay.ore * clay - bp.obsidian.ore * obs - bp.geode.ore * geo,
                clay=inventory.clay + inventory.robot_clay - bp.obsidian.clay * obs,
                obsidian=inventory.obsidian + inventory.robot_obsidian - bp.geode.obsidian * geo,
                geode=inventory.geode + inventory.robot_geode,
                robot_ore=inventory.robot_ore + ore,
                robot_clay=inventory.robot_clay + clay,
                robot_obsidian=inventory.robot_obsidian + obs,
                robot_geode=inventory.robot_geode + geo,
            )

            result = dfs(t + 1, candidate, best_result=best_result)
            if result.geode > best_result.geode:
                best_result = result

        return best_result

    result = dfs(t=1, inventory=Inventory(), best_result=Inventory())
    print(bp.id, result)
    return bp.id * result.geode


def main():
    with open(sys.argv[1], "r") as f:
        blueprints = [[x for x in re.split(r":| ", line) if x.isdigit()] for line in f.read().split("\n")]
        blueprints = [Blueprint.make(*blueprint) for blueprint in blueprints]

        print("part1:", sum(search(bp, 24, verbose=True) for bp in blueprints))


if __name__ == "__main__":
    main()
