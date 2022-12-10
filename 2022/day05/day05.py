import sys

with open(sys.argv[1], "r") as f:
    raw_crates, raw_instructions = f.read().split("\n\n")
    crates = [x[1::4] for x in raw_crates.split("\n")]
    pos, idx = crates[:-1][::-1], crates[-1]
    stacks = {int(i): "".join([x[ix] for x in pos]).strip() for ix, i in enumerate(idx)}

    print("start")
    print(stacks)

    instructions = raw_instructions.split("\n")
    for instruction in instructions:
        print(instruction)
        n, src, dst = [int(x) for x in instruction.split(" ")[1::2]]

        stacks[dst] = stacks[dst] + stacks[src][-n:]
        stacks[src] = stacks[src][:-n]

        print(stacks)
        print("---")

    print("\nanswer")
    for k, v in stacks.items():
        print(v[-1], end="")
    print()
    print("HNSNMTLHQ")
