from collections import defaultdict
import math
import re


def get_winning_sum() -> int:
    winning_sum = 0
    with open("data.txt") as data_file:
        for line in data_file:
            card_match = re.match("Card *\d+: ([0-9 ]+)\| ([0-9 ]+)", line)
            winning_nums = {
                int(num) for num in card_match.group(1).split(" ") if num != ""
            }
            game_nums = {
                int(num) for num in card_match.group(2).split(" ") if num != ""
            }
            num_matches = len(winning_nums & game_nums)
            if num_matches > 0:
                winning_sum += int(math.pow(2, num_matches - 1))
    return winning_sum


def get_total_cards() -> int:
    winning_index = {}
    with open("data.txt") as data_file:
        line_num = 0
        for line in data_file:
            card_match = re.match("Card *\d+: ([0-9 ]+)\| ([0-9 ]+)", line)
            winning_nums = {
                int(num) for num in card_match.group(1).split(" ") if num != ""
            }
            game_nums = {
                int(num) for num in card_match.group(2).split(" ") if num != ""
            }
            num_matches = len(winning_nums & game_nums)
            winning_index[line_num] = num_matches
            line_num += 1

    total_cards = 0
    num_cards_at_index = defaultdict(lambda: 1)
    for i in range(line_num):
        total_cards += num_cards_at_index[i]
        for j in range(1, winning_index[i] + 1):
            num_cards_at_index[i + j] += num_cards_at_index[i]

    return total_cards


if __name__ == "__main__":
    print(get_total_cards())
