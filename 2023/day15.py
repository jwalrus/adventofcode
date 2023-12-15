from collections import OrderedDict


def hash_(s) -> int:
    result = 0
    for c in s:
        result += ord(c)
        result *= 17
        result %= 256
    return result


def part1(steps):
    return sum(hash_(step) for step in steps)


def part2(steps):
    boxes = {i: OrderedDict() for i in range(256)}
    for step in steps:
        if "=" in step:
            label, focal_len = step.split("=")
            boxes[hash_(label)][label] = int(focal_len)
        else:
            label, _ = step.split("-")
            boxes[hash_(label)] = {l: f for l, f in boxes[hash_(label)].items() if l != label}

    result = 0
    for k, v in boxes.items():
        if v:
            for j, (lb, fl) in enumerate(v.items()):
                # print(lb, k + 1, j + 1, fl)
                result += (k + 1) * (j + 1) * fl

    return result


def main():
    with open(0) as f:
        steps = f.read().strip().split(",")
    print("A:", part1(steps))  # 508,498
    print("B:", part2(steps))  # 279,116


if __name__ == '__main__':
    main()
