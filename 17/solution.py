from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from heapq import heapify, heappush, heappop

AUTO_INCREMENT = 0


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    NONE = 5


@dataclass
class Path:
    position: tuple[int, int]
    direction: Direction
    cost: int
    min_remaining_cost: int
    num_steps_in_same_direction: int
    all_positions: list[tuple[int, int, Direction]]

    def __repr__(self) -> str:
        return f"({self.position}, {self.direction}, {self.cost}, {self.num_steps_in_same_direction})"


def parse_data():
    grid = []
    with open("data.txt") as data_file:
        for line in data_file:
            grid.append([int(pos) for pos in list(line.strip())])
    return grid


def is_valid_position(x, y, grid):
    return x >= 0 and x < len(grid) and y >= 0 and y < len(grid[0])


def get_min_remaining_cost(grid, position):
    return len(grid) - position[0] + len(grid[0]) - position[1]


def part1(min_steps, max_steps):
    global AUTO_INCREMENT

    grid = parse_data()
    initial_path = Path(
        (0, 0),
        Direction.NONE,
        0,
        get_min_remaining_cost(grid, (0, 0)),
        0,
        [(0, 0, Direction.NONE)],
    )
    heap = [
        (
            initial_path.cost + initial_path.min_remaining_cost,
            AUTO_INCREMENT,
            initial_path,
        )
    ]
    AUTO_INCREMENT += 1
    heapify(heap)
    visited = set()
    while heap:
        _, _, path = heappop(heap)

        if (path.position, path.direction, path.num_steps_in_same_direction) in visited:
            continue

        visited.add((path.position, path.direction, path.num_steps_in_same_direction))

        row, col = path.position
        valid_directions = (
            [path.direction] if path.num_steps_in_same_direction < max_steps else []
        )
        if path.direction == Direction.NONE:
            valid_directions = [Direction.RIGHT, Direction.DOWN]
        elif (
            path.direction in (Direction.UP, Direction.DOWN)
            and path.num_steps_in_same_direction >= min_steps
        ):
            valid_directions.extend([Direction.LEFT, Direction.RIGHT])
        elif (
            path.direction in (Direction.LEFT, Direction.RIGHT)
            and path.num_steps_in_same_direction >= min_steps
        ):
            valid_directions.extend([Direction.UP, Direction.DOWN])
        for direction in valid_directions:
            if direction == Direction.UP:
                new_row, new_col = row - 1, col
            elif direction == Direction.RIGHT:
                new_row, new_col = row, col + 1
            elif direction == Direction.DOWN:
                new_row, new_col = row + 1, col
            elif direction == Direction.LEFT:
                new_row, new_col = row, col - 1

            if (new_row, new_col) == (len(grid) - 1, len(grid[0]) - 1):
                final_path = Path(
                    (new_row, new_col),
                    direction,
                    path.cost + grid[new_row][new_col],
                    get_min_remaining_cost(grid, (new_row, new_col)),
                    path.num_steps_in_same_direction + 1
                    if direction == path.direction
                    else 1,
                    path.all_positions + [(new_row, new_col, direction)],
                )
                draw_grid(grid, final_path.all_positions)
                return final_path.cost

            new_steps_in_same_direction = (
                path.num_steps_in_same_direction + 1
                if direction == path.direction
                else 1
            )
            if (
                is_valid_position(new_row, new_col, grid)
                and (
                    (new_row, new_col),
                    direction,
                    new_steps_in_same_direction,
                )
                not in visited
            ):
                new_path = Path(
                    (new_row, new_col),
                    direction,
                    path.cost + grid[new_row][new_col],
                    get_min_remaining_cost(grid, (new_row, new_col)),
                    new_steps_in_same_direction,
                    path.all_positions + [(new_row, new_col, direction)],
                )
                heappush(
                    heap,
                    (new_path.cost + path.min_remaining_cost, AUTO_INCREMENT, new_path),
                )
                AUTO_INCREMENT += 1

    return None


def draw_grid(grid, all_positions):
    new_grid = deepcopy(grid)
    for row, col, direction in all_positions:
        new_char = "*"
        if direction == Direction.UP:
            new_char = "^"
        elif direction == Direction.RIGHT:
            new_char = ">"
        elif direction == Direction.DOWN:
            new_char = "v"
        elif direction == Direction.LEFT:
            new_char = "<"
        new_grid[row][col] = new_char
    for row in new_grid:
        print("".join([str(r) for r in row]))


def part2():
    return part1(4, 10)


if __name__ == "__main__":
    print(part1(1, 3))
    print(part2())
