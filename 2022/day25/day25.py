import sys

snafu_to_dec = {
    "2": 2,
    "1": 1,
    "0": 0,
    "=": -2,
    "-": -1,
}

dec_to_snafu = {v: k for k, v in snafu_to_dec.items()}


def snafu(xs: int) -> str:
    result = ""
    while xs != 0:
        # "rotating" 1, 2, 3, 4, 5 to -2, -1, 0, 1, 2
        x = (xs + 2) % 5 - 2
        result += dec_to_snafu[x]
        xs = (xs - x) // 5

    return result[::-1]


def decimal(xs: str) -> str:
    return sum(5 ** i * snafu_to_dec[x] for i, x in enumerate(xs[::-1]))


def main():
    with open(sys.argv[1], "r") as f:
        lines = f.read().split("\n")
        result = sum(decimal(x) for x in lines)
        print("decimal:", result)
        print("snafu:", snafu(result))


if __name__ == "__main__":
    main()
