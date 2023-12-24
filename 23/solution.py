def is_valid(grid: list[list[str]], position: tuple[int, int]):
    return (
        position[0] >= 0
        and position[0] < len(grid)
        and position[1] >= 0
        and position[1] < len(grid[0])
    )


class Path:
    def __init__(self, visited: set[tuple[int, int]], current: tuple[int, int]):
        self.visited = visited
        self.current = current

    def get_neighbors(self, grid: list[list[str]], avoid_slopes: bool):
        # Welp, this took way too long to run on the full input, so the avoid_slopes
        # approach is a bust. I'm going to try to solve this with a different approach.
        all_neighbors = [
            (self.current[0] + 1, self.current[1]),
            (self.current[0], self.current[1] + 1),
            (self.current[0] - 1, self.current[1]),
            (self.current[0], self.current[1] - 1),
        ]
        if not avoid_slopes:
            return all_neighbors

        curr_char = grid[self.current[0]][self.current[1]]
        if curr_char == ">":
            return [(self.current[0], self.current[1] + 1)]
        elif curr_char == "<":
            return [(self.current[0], self.current[1] - 1)]
        elif curr_char == "^":
            return [(self.current[0] - 1, self.current[1])]
        elif curr_char == "v":
            return [(self.current[0] + 1, self.current[1])]
        else:
            return all_neighbors

    def get_next_paths(self, grid: list[list[str]], avoid_slopes: bool):
        neighbors = self.get_neighbors(grid, avoid_slopes)
        next_paths = []
        for neighbor in neighbors:
            if (
                is_valid(grid, neighbor)
                and neighbor not in self.visited
                and grid[neighbor[0]][neighbor[1]] != "#"
            ):
                next_paths.append(Path(self.visited.union({neighbor}), neighbor))

        return next_paths

    @property
    def length(self):
        return len(self.visited) - 1


def parse_input():
    grid = []
    with open("data.txt") as f:
        for line in f:
            grid.append(list(line.strip()))
    return grid


def explore(avoid_slopes: bool):
    grid = parse_input()

    start = (0, 1)
    end = (len(grid) - 1, len(grid[0]) - 2)
    paths_to_explore = [Path({start}, start)]
    longest_path_to_end = 0
    while paths_to_explore:
        path = paths_to_explore.pop()
        if path.current == end:
            longest_path_to_end = max(longest_path_to_end, path.length)
        else:
            paths_to_explore.extend(path.get_next_paths(grid, avoid_slopes))
    return longest_path_to_end


class Node:
    def __init__(self, position: tuple[int, int], next_steps: list[tuple[int, int]]):
        self.position = position
        self.neighbors = {}
        self.next_steps = next_steps

    def add_neighbor(self, neighbor: tuple[int, int], cost: int):
        self.neighbors[neighbor] = cost

    def __repr__(self):
        return f"Node({self.position}, {self.neighbors})"


def get_outbound_path_steps(grid: list[list[str]], x: int, y: int):
    all_neighbors = [
        (x + 1, y),
        (x, y + 1),
        (x - 1, y),
        (x, y - 1),
    ]
    valid_neighbors = []
    for neighbor in all_neighbors:
        if is_valid(grid, neighbor) and grid[neighbor[0]][neighbor[1]] != "#":
            valid_neighbors.append(neighbor)
    return valid_neighbors


def convert_grid_to_graph(grid: list[list[str]]):
    graph = {}
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char != "#":
                valid_neighbors = get_outbound_path_steps(grid, i, j)
                if len(valid_neighbors) > 2:
                    graph[(i, j)] = Node((i, j), valid_neighbors)
                elif (i, j) in [(0, 1), (len(grid) - 1, len(grid[0]) - 2)]:
                    graph[(i, j)] = Node((i, j), valid_neighbors)

    return graph


def build_neighbors(grid: list[list[str]], graph: dict[tuple[int, int], Node]):
    for node_pos, node in graph.items():
        for next_step in node.next_steps:
            curr_step = next_step
            visited = {node_pos}
            while next_step not in graph:
                visited.add(next_step)
                potential_next_steps = get_outbound_path_steps(
                    grid, next_step[0], next_step[1]
                )
                actual_next_steps = set(potential_next_steps).difference(visited)
                if len(actual_next_steps) > 1:
                    raise Exception("Too many next steps")
                next_step = list(actual_next_steps)[0]
            node.add_neighbor(next_step, len(visited))


def print_grid_with_nodes(grid: list[list[str]], graph: dict[tuple[int, int], Node]):
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if (i, j) in graph:
                print("N", end="")
            else:
                print(char, end="")
        print()


def part1():
    return explore(avoid_slopes=True)


def part2():
    grid = parse_input()
    graph = convert_grid_to_graph(grid)

    build_neighbors(grid, graph)

    start = graph[(0, 1)]
    end = graph[(len(grid) - 1, len(grid[0]) - 2)]
    paths_to_explore = [(start, {start}, 0)]
    longest_path_to_end = 0
    while paths_to_explore:
        path = paths_to_explore.pop()
        curr_node, visited, cost = path
        if curr_node == end:
            longest_path_to_end = max(longest_path_to_end, cost)
        else:
            for neighbor in curr_node.neighbors:
                if neighbor not in visited:
                    paths_to_explore.append(
                        (
                            graph[neighbor],
                            visited.union({neighbor}),
                            cost + curr_node.neighbors[neighbor],
                        )
                    )

    return longest_path_to_end


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
