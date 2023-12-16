from collections import defaultdict
from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


@dataclass
class Light:
    x: int
    y: int
    direction: Direction

    def get_position(self):
        return (self.x, self.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.direction})"


def should_continue(grid, visited, light):
    x, y = light.get_position()
    return (
        x >= 0
        and x < len(grid)
        and y >= 0
        and y < len(grid[0])
        and ((x, y) not in visited or light.direction not in visited[(x, y)])
    )


def get_next_lights(grid, light):
    x, y = light.get_position()
    directions = [light.direction]
    if grid[x][y] == "/":
        if light.direction == Direction.UP:
            directions = [Direction.RIGHT]
        elif light.direction == Direction.RIGHT:
            directions = [Direction.UP]
        elif light.direction == Direction.DOWN:
            directions = [Direction.LEFT]
        elif light.direction == Direction.LEFT:
            directions = [Direction.DOWN]
    elif grid[x][y] == "\\":
        if light.direction == Direction.UP:
            directions = [Direction.LEFT]
        elif light.direction == Direction.RIGHT:
            directions = [Direction.DOWN]
        elif light.direction == Direction.DOWN:
            directions = [Direction.RIGHT]
        elif light.direction == Direction.LEFT:
            directions = [Direction.UP]
    elif grid[x][y] == "|":
        if light.direction in (Direction.LEFT, Direction.RIGHT):
            directions = [Direction.UP, Direction.DOWN]
    elif grid[x][y] == "-":
        if light.direction in (Direction.UP, Direction.DOWN):
            directions = [Direction.RIGHT, Direction.LEFT]

    positions = []
    for direction in directions:
        if direction == Direction.UP:
            positions.append(Light(x - 1, y, direction))
        elif direction == Direction.RIGHT:
            positions.append(Light(x, y + 1, direction))
        elif direction == Direction.DOWN:
            positions.append(Light(x + 1, y, direction))
        elif direction == Direction.LEFT:
            positions.append(Light(x, y - 1, direction))

    return positions


def run_light(light, grid):
    visited = defaultdict(set)

    to_explore = [light]
    while to_explore:
        curr_light = to_explore.pop()
        while should_continue(grid, visited, curr_light):
            visited[curr_light.get_position()].add(curr_light.direction)
            next_lights = get_next_lights(grid, curr_light)
            if len(next_lights) > 1:
                to_explore.append(next_lights[1])
            curr_light = next_lights[0]

    return len([v for v in visited.keys() if len(visited[v]) > 0])


def part1():
    grid = []
    with open("data.txt") as data_file:
        for line in data_file:
            grid.append(list(line.strip()))
    return run_light(Light(0, 0, Direction.RIGHT), grid)


def part2():
    grid = []
    with open("data.txt") as data_file:
        for line in data_file:
            grid.append(list(line.strip()))

    max_energized = 0
    for i in range(len(grid)):
        max_energized = max(
            max_energized, run_light(Light(i, 0, Direction.RIGHT), grid)
        )
        max_energized = max(
            max_energized, run_light(Light(i, len(grid[0]) - 1, Direction.LEFT), grid)
        )

    for i in range(len(grid[0])):
        max_energized = max(max_energized, run_light(Light(0, i, Direction.DOWN), grid))
        max_energized = max(
            max_energized, run_light(Light(len(grid) - 1, i, Direction.UP), grid)
        )

    return max_energized


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
