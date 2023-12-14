import re


def get_calibration_number(line: str) -> int:
    print(line)
    first_match = re.match("^\D*(\d).*", line)
    last_match = re.match(".*(\d)\D*$", line)
    first_group = first_match.group(1)
    last_group = last_match.group(1)

    (
        earliest_match,
        earliest_match_index,
        latest_match,
        latest_match_index,
    ) = get_text_match(line)

    first_digit = str(first_group)
    last_digit = str(last_group)

    if earliest_match_index is not None and earliest_match_index < first_match.start(1):
        first_digit = str(earliest_match)

    if latest_match_index is not None and latest_match_index > last_match.start(1):
        last_digit = str(latest_match)

    calibration_number = int(f"{first_digit}{last_digit}")
    print(f"Calibration_num : {calibration_number}")
    print("-------------")
    return calibration_number


def get_text_match(line):
    conversion_map = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
    }
    earliest_match_index = None
    earliest_match = None
    latest_match_index = None
    latest_match = None

    for digit, d_text in conversion_map.items():
        earliest_find = line.find(d_text)
        latest_find = line.rfind(d_text)
        if (
            earliest_match is None or earliest_find < earliest_match_index
        ) and earliest_find != -1:
            earliest_match = digit
            earliest_match_index = earliest_find
        if (
            latest_match is None or latest_find > latest_match_index
        ) and latest_find != -1:
            latest_match = digit
            latest_match_index = latest_find
    return earliest_match, earliest_match_index, latest_match, latest_match_index


def convert_line(line: str) -> str:
    conversion_map = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
    }
    (
        earliest_match,
        earliest_match_index,
        latest_match,
        latest_match_index,
    ) = get_text_match(line)
    new_line = line
    print(f"Earliest match: {earliest_match} @ {earliest_match_index}")
    print(f"Latest match: {latest_match} @ {latest_match_index}")

    if latest_match is not None:
        d_text = conversion_map[latest_match]
        new_line = (
            new_line[:latest_match_index]
            + str(latest_match)
            + new_line[latest_match_index + len(d_text) :]
        )
    print(f"NewLine: {new_line}")
    if earliest_match is not None and earliest_match_index != latest_match_index:
        d_text = conversion_map[earliest_match]
        new_line = (
            new_line[:earliest_match_index]
            + str(earliest_match)
            + new_line[earliest_match_index + len(d_text) :]
        )
    print(f"NewLine: {new_line}")
    return new_line


def find_calibration() -> int:
    with open("data.txt") as data_file:
        calibration_sum = 0
        for line in data_file:
            print("-------------")
            print(f"Line: {line}")
            # calibration_sum += get_calibration_number(convert_line(line))
            calibration_sum += get_calibration_number(line)
    return calibration_sum


if __name__ == "__main__":
    print(find_calibration())
