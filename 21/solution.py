from re import I


def parse_input():
    grid = []
    start = None
    even_rock_count = 0
    odd_rock_count = 0
    with open("data.txt") as f:
        for line in f:
            s_index = line.find("S")
            row_num = len(grid)
            if s_index != -1:
                start = (len(grid), s_index)

            row = list(line.strip())
            for col_num, c in enumerate(row):
                if c == "#":
                    if (row_num + col_num) % 2 == 0:
                        even_rock_count += 1
                    else:
                        odd_rock_count += 1
            grid.append(row)
    return grid, start, even_rock_count, odd_rock_count


def is_valid(grid, x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != "#"


def draw_grid(grid, found_positions):
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if (x, y) in found_positions:
                print("O", end="")
            else:
                print(grid[x][y], end="")
        print()


def part1(total_iterations=6):
    num_plots = 0
    grid, start, _, _ = parse_input()

    visited = set()
    curr_positions = [start]

    iterations = 0
    found_positions = set()
    while iterations <= total_iterations:
        next_positions = []
        while curr_positions:
            curr_position = curr_positions.pop()
            if curr_position in visited:
                continue

            visited.add(curr_position)

            x, y = curr_position
            if iterations % 2 == 0:
                found_positions.add(curr_position)
                num_plots += 1

            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if (dx == 0 and dy == 0) or (dx != 0 and dy != 0):
                        continue
                    if is_valid(grid, x + dx, y + dy):
                        next_positions.append((x + dx, y + dy))
        curr_positions = next_positions

        iterations += 1

    draw_grid(grid, found_positions)

    return num_plots


# Ended up identifying that this would be some kind of function based on
# the pattern of the grid. I didn't feel like actually figuring this part
# out, so I confirmed my guess with the subreddit and then didn't bother
# implementing it.
def part2():
    grid, start, even_rock_count, odd_rock_count = parse_input()
    print(f"Even: {even_rock_count}, Odd: {odd_rock_count}")


if __name__ == "__main__":
    print(f"Part1: {part1(total_iterations=64)}")
    print(f"Part2: {part2()}")
