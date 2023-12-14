from collections import defaultdict


def get_horizontal_reflection_rows(grid):
    row_hashes = defaultdict(set)
    for row_i in range(len(grid)):
        current_reflection = row_i - 1
        found_smudge = False
        forward_reflection_i = row_i
        while current_reflection >= 0 and forward_reflection_i < len(grid):
            row_hash = hash(grid[forward_reflection_i])
            diff_count = sum(
                1
                for a, b in zip(grid[forward_reflection_i], grid[current_reflection])
                if a != b
            )
            if diff_count == 1 and not found_smudge:
                found_smudge = True
            elif diff_count > 0 or current_reflection not in row_hashes[row_hash]:
                break
            current_reflection -= 1
            forward_reflection_i += 1
            if (
                current_reflection == -1 or forward_reflection_i == len(grid)
            ) and found_smudge:
                return row_i

        row_hashes[hash(grid[row_i])].add(row_i)


def get_vertical_reflection_columns(grid):
    return get_horizontal_reflection_rows(list(zip(*grid[::-1])))


def get_reflection_num(grid):
    reflection_num = get_horizontal_reflection_rows(grid)
    if reflection_num is not None:
        return 100 * reflection_num
    return get_vertical_reflection_columns(grid)


def solution():
    total_sum = 0
    with open("data.txt") as data_file:
        grid = []
        for line in data_file:
            if line != "\n":
                grid.append(line.strip())
            else:
                total_sum += get_reflection_num(grid)
                grid = []
        total_sum += get_reflection_num(grid)

    return total_sum


if __name__ == "__main__":
    print(solution())
