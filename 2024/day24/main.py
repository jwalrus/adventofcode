import sys
from collections import deque
from operator import and_, or_, xor

OPS = {"AND": and_, "OR": or_, "XOR": xor}


def main():
    with open(sys.argv[1]) as f:
        wire_values, gates = f.read().split("\n\n")
    wire_values = (wv.split(": ") for wv in wire_values.splitlines())
    wire_values = {k: int(v) for k, v in wire_values}
    gates = (g.replace(" -> ", " ").split(" ") for g in gates.splitlines())
    gates = [(OPS[o], l, r, d) for l, o, r, d in gates]

    print("part1:", part1(wire_values, gates))
    print("part2:", ",".join(part2(gates)))


def part1(wire_values, gates):
    queue = deque(gates)

    while queue:
        op, l, r, d = queue.popleft()
        if wire_values.get(l) is not None and wire_values.get(r) is not None:
            wire_values[d] = op(wire_values[l], wire_values[r])
        else:
            queue.append((op, l, r, d))

    zs = sorted([(k, v) for k, v in wire_values.items() if k.startswith("z")], reverse=True)
    z = "".join(str(z[1]) for z in zs)
    return int(z, 2)


def part2(gates):
    # https://circuitfever.com/ripple-carry-adder
    bad = set()
    for op, lf, rt, dst in gates:
        # first case is special
        if lf in ("x00", "y00") or rt in ("x00", "y00"):
            if op.__name__ == "xor" and dst[0] != "z":
                bad.add(dst)
                continue
            if op.__name__ == "and_":
                for op2, lf2, rt2, dst2 in gates:
                    if (dst == lf2 or dst == rt2) and op2.__name__ == "or_":
                        bad.add(dst)
            continue

        # last load is special
        if dst[0] == "z" and op.__name__ != "xor" and dst != "z45":
            bad.add(dst)

        match op.__name__:
            case "xor":
                # result of XOR cannot feed to OR
                for op2, lf2, rt2, dst2 in gates:
                    if (dst == lf2 or dst == rt2) and op2.__name__ == "or_":
                        bad.add(dst)
                # input of XOR must X/Y or output must be Z
                if dst[0] != "z" and (lf[0] not in ("x", "y") or rt[0] not in ("x", "y")):
                    bad.add(dst)
            case "and_":
                # result of AND must feed to OR
                for op2, lf2, rt2, dst2 in gates:
                    if (dst == lf2 or dst == rt2) and op2.__name__ != "or_":
                        bad.add(dst)

            case "or_":
                # result of OR cannot feed to OR
                for op2, lf2, rt2, dst2 in gates:
                    if (dst == lf2 or dst == rt2) and op2.__name__ == "or":
                        bad.add(dst)

    return sorted(bad)


if __name__ == '__main__':
    main()
