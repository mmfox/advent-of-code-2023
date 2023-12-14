from dataclasses import dataclass
import re


@dataclass
class ShowCount:
    red: int
    green: int
    blue: int


@dataclass
class GameData:
    id: int
    counts: list[ShowCount]

    def max_count(self) -> ShowCount:
        max_show_count = ShowCount(0, 0, 0)
        for count in self.counts:
            max_show_count.red = max(max_show_count.red, count.red)
            max_show_count.green = max(max_show_count.green, count.green)
            max_show_count.blue = max(max_show_count.blue, count.blue)

        return max_show_count


def calculate_games_sum(game_parameters: ShowCount) -> int:
    games_sum = 0
    with open("data.txt") as data_file:
        for line in data_file:
            game_data = parse_game(line)
            max_count = game_data.max_count()

            print(f"Line: {line}\nGameData: {game_data}\nMaxCount: {max_count}\n\n")

            if (
                max_count.red <= game_parameters.red
                and max_count.green <= game_parameters.green
                and max_count.blue <= game_parameters.blue
            ):
                games_sum += game_data.id
    return games_sum


def calculate_games_power() -> int:
    games_sum = 0
    with open("data.txt") as data_file:
        for line in data_file:
            game_data = parse_game(line)
            max_count = game_data.max_count()
            games_sum += max_count.red * max_count.blue * max_count.green
    return games_sum


def parse_game(line: str) -> GameData:
    id_match = re.match("Game (\d+).*", line)
    id = int(id_match.group(1))
    pulls = line[id_match.end(1) + 1 :].split(";")
    counts = []
    for pull in pulls:
        red_match = re.match(".* (\d+) red.*", pull)
        red_count = int(red_match.group(1)) if red_match is not None else 0
        blue_match = re.match(".* (\d+) blue.*", pull)
        blue_count = int(blue_match.group(1)) if blue_match is not None else 0
        green_match = re.match(".* (\d+) green.*", pull)
        green_count = int(green_match.group(1)) if green_match is not None else 0
        counts.append(ShowCount(red_count, green_count, blue_count))
    return GameData(id, counts)


if __name__ == "__main__":
    game_parameters = ShowCount(12, 13, 14)
    # print(calculate_games_sum(game_parameters))
    print(calculate_games_power())
