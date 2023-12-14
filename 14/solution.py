from collections import defaultdict


def print_grid(grid):
    for row in grid:
        print("".join(row))
    print("\n\n")


def part1():
    load_factor = 0
    next_available_slots = defaultdict(lambda: len(grid) - 1)
    grid = []
    with open("data.txt") as data_file:
        for line in data_file:
            grid.append([c for c in line.strip()])

    next_available_slots = defaultdict(int)
    for row_i in range(len(grid)):
        for col_i in range(len(grid[row_i])):
            char = grid[row_i][col_i]
            if char == "#":
                next_available_slots[col_i] = row_i + 1
            elif char == "O":
                load_factor += len(grid) - next_available_slots[col_i]
                if next_available_slots[col_i] != row_i:
                    grid[row_i][col_i] = "."
                    grid[next_available_slots[col_i]][col_i] = "O"
                next_available_slots[col_i] += 1

    return load_factor


def calculate_load_factor(grid):
    load_factor = 0
    for row_i, row in enumerate(grid):
        for char in row:
            if char == "O":
                load_factor += len(grid) - row_i
    return load_factor


def run_cycles(grid, num_cycles):
    known_grids = {}
    cycles_remaining = None
    for cycle in range(num_cycles):
        # Identify if we've seen this grid before and how many more cycles we should run before we're done.
        grid_hash = hash(str(grid))
        if cycles_remaining is None and grid_hash in known_grids:
            cycle_length = cycle - known_grids[grid_hash]
            final_cycle_off = num_cycles % cycle_length
            curr_cycle_off = cycle % cycle_length
            cycles_remaining = final_cycle_off - curr_cycle_off
            if cycles_remaining < 0:
                cycles_remaining += cycle_length
            print(
                f"Found cycle: {cycle} - {known_grids[grid_hash]}.  Will continue for {cycles_remaining} more cycles"
            )

        if cycles_remaining == 0:
            return calculate_load_factor(grid)
        elif cycles_remaining is not None:
            cycles_remaining -= 1
        known_grids[grid_hash] = cycle

        # North
        next_available_slots = defaultdict(int)
        for row_i in range(len(grid)):
            for col_i in range(len(grid[row_i])):
                char = grid[row_i][col_i]
                if char == "#":
                    next_available_slots[col_i] = row_i + 1
                elif char == "O":
                    if next_available_slots[col_i] != row_i:
                        grid[row_i][col_i] = "."
                        grid[next_available_slots[col_i]][col_i] = "O"
                    next_available_slots[col_i] += 1

        # West
        next_available_slots = defaultdict(int)
        for row_i in range(len(grid)):
            for col_i in range(len(grid[row_i])):
                char = grid[row_i][col_i]
                if char == "#":
                    next_available_slots[row_i] = col_i + 1
                elif char == "O":
                    if next_available_slots[row_i] != col_i:
                        grid[row_i][col_i] = "."
                        grid[row_i][next_available_slots[row_i]] = "O"
                    next_available_slots[row_i] += 1

        # South
        next_available_slots = defaultdict(lambda: len(grid) - 1)
        for row_i in range(len(grid) - 1, -1, -1):
            for col_i in range(len(grid[row_i])):
                char = grid[row_i][col_i]
                if char == "#":
                    next_available_slots[col_i] = row_i - 1
                elif char == "O":
                    if next_available_slots[col_i] != row_i:
                        grid[row_i][col_i] = "."
                        grid[next_available_slots[col_i]][col_i] = "O"
                    next_available_slots[col_i] -= 1

        # East
        next_available_slots = defaultdict(lambda: len(grid[0]) - 1)
        for row_i in range(len(grid)):
            for col_i in range(len(grid[row_i]) - 1, -1, -1):
                char = grid[row_i][col_i]
                if char == "#":
                    next_available_slots[row_i] = col_i - 1
                elif char == "O":
                    if next_available_slots[row_i] != col_i:
                        grid[row_i][col_i] = "."
                        grid[row_i][next_available_slots[row_i]] = "O"
                    next_available_slots[row_i] -= 1

    return calculate_load_factor(grid)


def part2():
    grid = []
    with open("data.txt") as data_file:
        for line in data_file:
            grid.append([c for c in line.strip()])
    return run_cycles(grid, 1000000000)


if __name__ == "__main__":
    print(f"Part1: {part1()}")
    print(f"Part2: {part2()}")
