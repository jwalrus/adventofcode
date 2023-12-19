def determinant(x1, y1, x2, y2):
    return x1 * y2 - x2 * y1


def shoelace(points):
    # https://en.wikipedia.org/wiki/Shoelace_formula
    xs = points + [points[0]]
    result = 0
    for x, y in zip(xs, xs[1:]):
        result += determinant(*x, *y)
    return result // 2


def picks(points, b):
    # https://en.wikipedia.org/wiki/Pick's_theorem
    # A = i + b / 2 - 1
    #   => i = A - b/2 + 1
    return shoelace(points) - b // 2 + 1 + b


def part1(instructions):
    points = []
    x, y = 0, 0
    points.append((x, y))
    perimeter = 0
    for _, (direction, dist, _) in enumerate(instructions):
        dist = int(dist)
        match direction:
            case "U":
                x, y = x, y + dist
            case "R":
                x, y = x + dist, y
            case "D":
                x, y = x, y - dist
            case "L":
                x, y = x - dist, y
        points.append((x, y))
        perimeter += dist
    return picks(points[::-1], b=perimeter)


def part2(instructions):
    hex_instructions = []
    for _, _, color in instructions:
        distance, direction = int(color[2:7], base=16), color[7]
        match direction:
            case "0":
                direction = "R"
            case "1":
                direction = "D"
            case "2":
                direction = "L"
            case "3":
                direction = "U"
        hex_instructions.append((direction, distance, color))

    return part1(hex_instructions)


def main():
    with open(0) as f:
        lines = f.read().splitlines()
    instructions = [line.split(" ") for line in lines]

    print("A:", part1(instructions))  # 48503
    print("B:", part2(instructions))  # 148442153147147


if __name__ == '__main__':
    main()
