from collections import defaultdict
import math

DIGITS = set()
for i in range(10):
    DIGITS.add(str(i))
NON_SYMBOLS = {".", "\n"} | DIGITS


def get_symbol_index() -> dict[int, set[int]]:
    with open("data.txt") as data_file:
        symbol_index = defaultdict(set)
        line_num = 0
        for line in data_file:
            for i in range(len(line)):
                if line[i] not in NON_SYMBOLS:
                    symbol_index[line_num].add(i)
            line_num += 1
    return symbol_index


def get_part_num_sum() -> int:
    part_num_sum = 0

    symbol_index = get_symbol_index()
    with open("data.txt") as data_file:

        def should_add_num(part_num, line_num, start_index):
            print(
                f"Part Num: {part_num}, line_num: {line_num}, start_index: {start_index}"
            )
            if part_num is None:
                return False

            for line_i in range(line_num - 1, line_num + 2):
                for char_i in range(start_index - 1, start_index + len(part_num) + 1):
                    if char_i in symbol_index[line_i]:
                        return True

            return False

        line_num = 0
        for line in data_file:
            active_num = None
            for i in range(len(line)):
                char = line[i]
                if char in DIGITS:
                    if active_num is None:
                        active_num = [char, i]
                    else:
                        active_num[0] += char
                else:
                    if active_num is not None and should_add_num(
                        active_num[0], line_num, active_num[1]
                    ):
                        print(f"Adding {active_num[0]} to sum")
                        part_num_sum += int(active_num[0])
                    active_num = None
            if active_num is not None:
                if should_add_num(active_num[0], line_num, active_num[1]):
                    print(f"Adding {active_num[0]} to sum from end of line")
                    part_num_sum += int(active_num[0])

            line_num += 1

    return part_num_sum


def get_gear_ratio() -> int:
    symbol_dict = {}
    with open("data.txt") as data_file:
        line_num = 0
        for line in data_file:
            for i in range(len(line)):
                char = line[i]
                if char == "*":
                    symbol_dict[(line_num, i)] = set()
            line_num += 1

    def add_to_symbol_dict(part_num, line_num, start_index):
        for line_i in range(line_num - 1, line_num + 2):
            for char_i in range(start_index - 1, start_index + len(part_num) + 1):
                print(f"Checking {(line_i, char_i)}")
                if (line_i, char_i) in symbol_dict:
                    symbol_dict[(line_i, char_i)].add(int(part_num))

    with open("data.txt") as data_file:
        line_num = 0
        for line in data_file:
            active_num = None
            for i in range(len(line)):
                char = line[i]
                if char in DIGITS:
                    if active_num is None:
                        active_num = [char, i]
                    else:
                        active_num[0] += char
                else:
                    if active_num is not None:
                        add_to_symbol_dict(active_num[0], line_num, active_num[1])
                    active_num = None
            if active_num is not None:
                add_to_symbol_dict(active_num[0], line_num, active_num[1])
            line_num += 1

    print(symbol_dict)
    total_sum = 0
    for adj_nums in symbol_dict.values():
        if len(adj_nums) == 2:
            total_sum += math.prod(adj_nums)

    return total_sum


if __name__ == "__main__":
    print(get_gear_ratio())
