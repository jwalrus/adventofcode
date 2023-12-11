lookup = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def find_digits(s: str, *, d: dict) -> int:
    digits = []
    for i, c in enumerate(s):
        if c.isdigit():
            digits.append(int(c))
        else:
            for k, v in d.items():
                if s[i:].startswith(k):
                    digits.append(v)
    return digits[0] * 10 + digits[-1]


if __name__ == "__main__":
    with open("z_day1.txt", "r") as f:
        lines = f.readlines()

    result_a = sum(find_digits(line, d={}) for line in lines)
    result_b = sum(find_digits(line, d=lookup) for line in lines)

    print("A", result_a)  # 55447
    print("B", result_b)  # 54706