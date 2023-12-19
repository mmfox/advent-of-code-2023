from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Instruction:
    dir: str
    dist: int


@dataclass
class Boundary:
    col: int
    is_corner: bool
    dir: str


def parse_input1():
    instructions = []
    with open("data.txt") as data_file:
        lines = data_file.readlines()
        for line in lines:
            dir, dist, color = line.strip().split(" ")
            instructions.append(Instruction(dir, int(dist)))

    return instructions


def parse_input2():
    instructions = []
    with open("data.txt") as data_file:
        lines = data_file.readlines()
        for line in lines:
            _, _, color = line.strip().split(" ")
            hex_num = color[2:-2]
            dir_code = int(color[-2])
            if dir_code == 0:
                dir = "R"
            elif dir_code == 1:
                dir = "D"
            elif dir_code == 2:
                dir = "L"
            elif dir_code == 3:
                dir = "U"
            dist = int(hex_num, 16)
            instructions.append(Instruction(dir, int(dist)))

    return instructions


def calc_space(instructions):
    min_row, max_row, min_col, max_col = None, None, None, None

    curr_row, curr_col = 0, 0
    row_boundaries = defaultdict(dict)
    for instruction in instructions:
        if instruction.dir == "U":
            row_boundaries[curr_row][curr_col] = Boundary(curr_col, True, "U")
            for row_i in range(curr_row - 1, curr_row - instruction.dist, -1):
                row_boundaries[row_i][curr_col] = Boundary(curr_col, False, "U")
            curr_row = curr_row - instruction.dist
            row_boundaries[curr_row][curr_col] = Boundary(curr_col, True, "U")
            min_row = min(min_row, curr_row) if min_row else curr_row
        elif instruction.dir == "D":
            row_boundaries[curr_row][curr_col] = Boundary(curr_col, True, "D")
            for row_i in range(curr_row + 1, curr_row + instruction.dist):
                row_boundaries[row_i][curr_col] = Boundary(curr_col, False, "D")
            curr_row = curr_row + instruction.dist
            row_boundaries[curr_row][curr_col] = Boundary(curr_col, True, "D")
            max_row = max(max_row, curr_row) if max_row else curr_row
        elif instruction.dir == "L":
            curr_col = curr_col - instruction.dist
            min_col = min(min_col, curr_col) if min_col else curr_col
        elif instruction.dir == "R":
            curr_col = curr_col + instruction.dist
            max_col = max(max_col, curr_col) if max_col else curr_col

    total_space = 0
    for row_i, boundaries in row_boundaries.items():
        last_boundary = None
        is_in = False
        on_boundary = False
        for col_i in sorted(boundaries.keys()):
            new_boundary = boundaries[col_i]
            if is_in:
                total_space += new_boundary.col - last_boundary.col
                if not new_boundary.is_corner or (
                    last_boundary and new_boundary.dir == last_boundary.dir
                ):
                    total_space += 1
                    is_in = False
            else:
                if not new_boundary.is_corner or (
                    last_boundary and new_boundary.dir == last_boundary.dir
                ):
                    is_in = True
                    if new_boundary.is_corner and on_boundary:
                        total_space += new_boundary.col - last_boundary.col
                    on_boundary = False
                elif new_boundary.is_corner:
                    if on_boundary:
                        total_space += new_boundary.col - last_boundary.col + 1
                        on_boundary = False
                    else:
                        on_boundary = True

            last_boundary = new_boundary

    return total_space


def part1():
    instructions = parse_input1()
    return calc_space(instructions)


def part2():
    instructions = parse_input2()
    return calc_space(instructions)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 1: {part2()}")
