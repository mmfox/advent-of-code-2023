def part1(gap=1):
    with open("data.txt") as data_file:
        data = data_file.read().splitlines()

        galaxy_coords = []
        columns_to_expand = {i for i in range(len(data[0]))}
        rows_to_expand = set()
        for i, row in enumerate(data):
            has_galaxy = False
            for j, symbol in enumerate(row):
                if symbol == "#":
                    has_galaxy = True
                    galaxy_coords.append((i, j))
                    columns_to_expand.discard(j)
            if not has_galaxy:
                rows_to_expand.add(i)

        total_steps = 0
        for galaxy_i in range(len(galaxy_coords)):
            for galaxy_j in range(galaxy_i + 1, len(galaxy_coords)):
                i_coords = galaxy_coords[galaxy_i]
                j_coords = galaxy_coords[galaxy_j]
                steps = abs(j_coords[1] - i_coords[1]) + abs(j_coords[0] - i_coords[0])
                for row_i in range(i_coords[0], j_coords[0] + 1):
                    if row_i in rows_to_expand:
                        steps += gap - 1
                min_col = min(i_coords[1], j_coords[1])
                max_col = max(i_coords[1], j_coords[1])
                for col_i in range(min_col, max_col + 1):
                    if col_i in columns_to_expand:
                        steps += gap - 1
                total_steps += steps
        return total_steps


def part2():
    return part1(1000000)


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
