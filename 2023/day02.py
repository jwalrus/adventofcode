TARGET = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def parse_game_id(s: str) -> int:
    _, id_ = s.strip().split(" ")
    return int(id_)


def parse_game(s: str) -> list[dict]:
    result = []
    for game in s.split("; "):
        sub_games = game.strip().split(", ")
        d = {}
        for sub_game in sub_games:
            num, color = sub_game.split(" ")
            d[color] = int(num)
        result.append(d)
    return result


def parse(s: str):
    id_, game = s.split(": ")
    return parse_game_id(id_), parse_game(game)


def is_possible(draws: list[dict], ref: dict) -> bool:
    return all(
        draw.get("blue", 0) <= ref["blue"] and
        draw.get("green", 0) <= ref["green"] and
        draw.get("red", 0) <= ref["red"]
        for draw in draws
    )


def power(draws: list[dict]) -> int:
    blue = max(d.get("blue", 1) for d in draws)
    green = max(d.get("green", 1) for d in draws)
    red = max(d.get("red", 1) for d in draws)
    return blue * green * red


if __name__ == '__main__':
    with open("day2.txt", "r") as f:
        games = [parse(line) for line in f.read().split("\n")]

    result_a = sum(id_ for id_, game in games if is_possible(game, TARGET))
    result_b = sum(power(game) for _, game in games)

    print("A", result_a)  # 2149
    print("B", result_b)  # 71274
