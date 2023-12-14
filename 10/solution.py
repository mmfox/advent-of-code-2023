# Identify if neighbor of S connects to S
from tracemalloc import start


def connects_to_start(symbol, start_coordinate, symbol_coordinate):
    if symbol == "|":
        return start_coordinate[1] == symbol_coordinate[1]
    elif symbol == "-":
        return start_coordinate[0] == symbol_coordinate[0]
    elif symbol == "L":
        return (
            start_coordinate[0] == symbol_coordinate[0]
            and start_coordinate[1] == symbol_coordinate[1] + 1
        ) or (
            start_coordinate[0] == symbol_coordinate[0] - 1
            and start_coordinate[1] == symbol_coordinate[1]
        )
    elif symbol == "J":
        return (
            start_coordinate[0] == symbol_coordinate[0]
            and start_coordinate[1] == symbol_coordinate[1] - 1
        ) or (
            start_coordinate[0] == symbol_coordinate[0] - 1
            and start_coordinate[1] == symbol_coordinate[1]
        )
    elif symbol == "7":
        return (
            start_coordinate[0] == symbol_coordinate[0] - 1
            and start_coordinate[1] == symbol_coordinate[1]
        ) or (
            start_coordinate[0] == symbol_coordinate[0]
            and start_coordinate[1] == symbol_coordinate[1] - 1
        )
    elif symbol == "F":
        return (
            start_coordinate[0] == symbol_coordinate[0] + 1
            and start_coordinate[1] == symbol_coordinate[1]
        ) or (
            start_coordinate[0] == symbol_coordinate[0]
            and start_coordinate[1] == symbol_coordinate[1] + 1
        )
    else:
        return False


# Given a symbol, current coordinates and previous coordinate, return the next coordinate
# Symbol | is a vertical path, - is a horizontal path, L is a turn from top to right, J is a turn from top to left, 7 is a turn from left to bottom, and F is a turn from right to bottom
def get_next_coordinate(symbol, current_coordinate, previous_coordinate):
    if symbol == "|":
        if previous_coordinate[0] > current_coordinate[0]:
            return (current_coordinate[0] - 1, current_coordinate[1])
        return (current_coordinate[0] + 1, current_coordinate[1])
    elif symbol == "-":
        if previous_coordinate[1] > current_coordinate[1]:
            return (current_coordinate[0], current_coordinate[1] - 1)
        return (current_coordinate[0], current_coordinate[1] + 1)
    elif symbol == "L":
        if previous_coordinate[0] == current_coordinate[0]:
            return (current_coordinate[0] - 1, current_coordinate[1])
        else:
            return (current_coordinate[0], current_coordinate[1] + 1)
    elif symbol == "J":
        if previous_coordinate[0] == current_coordinate[0]:
            return (current_coordinate[0] - 1, current_coordinate[1])
        else:
            return (current_coordinate[0], current_coordinate[1] - 1)
    elif symbol == "7":
        if previous_coordinate[0] == current_coordinate[0]:
            return (current_coordinate[0] + 1, current_coordinate[1])
        else:
            return (current_coordinate[0], current_coordinate[1] - 1)
    elif symbol == "F":
        if previous_coordinate[0] == current_coordinate[0]:
            return (current_coordinate[0] + 1, current_coordinate[1])
        else:
            return (current_coordinate[0], current_coordinate[1] + 1)


def is_valid_coordinate(coordinate, data):
    return (
        coordinate[0] >= 0
        and coordinate[0] < len(data)
        and coordinate[1] >= 0
        and coordinate[1] < len(data[0])
    )


def solution():
    path_coords = set()
    total_path_length = 0
    num_contained_coords = 0
    with open("data.txt") as data_file:
        start_location = None
        data = data_file.read().splitlines()
        for i, row in enumerate(data):
            if "S" in row:
                start_location = (i, row.index("S"))
                break
        last_coordinate = start_location
        curr_coordinate = None
        for i in range(start_location[0] - 1, start_location[0] + 2):
            if curr_coordinate:
                break
            for j in range(start_location[1] - 1, start_location[1] + 2):
                if is_valid_coordinate((i, j), data) and (i, j) != start_location:
                    if connects_to_start(data[i][j], start_location, (i, j)):
                        curr_coordinate = (i, j)
                        break

        path_coords.add(start_location)
        path_coords.add(curr_coordinate)
        while data[curr_coordinate[0]][curr_coordinate[1]] != "S":
            total_path_length += 1
            next_coordinate = get_next_coordinate(
                data[curr_coordinate[0]][curr_coordinate[1]],
                curr_coordinate,
                last_coordinate,
            )
            last_coordinate = curr_coordinate
            curr_coordinate = next_coordinate
            path_coords.add(curr_coordinate)

        for i in range(len(data)):
            num_edges_crossed = 0
            on_edge = False
            came_from_top = False
            for j in range(len(data[0])):
                if (i, j) in path_coords:
                    if data[i][j] == "|":
                        num_edges_crossed += 1
                    elif not on_edge and data[i][j] == "F":
                        came_from_top = False
                        on_edge = True
                    elif not on_edge and data[i][j] == "L":
                        came_from_top = True
                        on_edge = True
                    elif on_edge and data[i][j] == "7":
                        if came_from_top:
                            num_edges_crossed += 1
                        on_edge = False
                    elif on_edge and data[i][j] == "J":
                        if not came_from_top:
                            num_edges_crossed += 1
                        on_edge = False
                elif num_edges_crossed % 2 == 1:
                    num_contained_coords += 1
    return num_contained_coords


if __name__ == "__main__":
    print(solution())
