from calendar import c
from collections import defaultdict
from heapq import heappop, heappush


class Block:
    def __init__(self, name, corners):
        self.corners = corners
        self.name = name

    def __repr__(self):
        return f"Block {self.name} with corners {self.corners}"

    def get_x_y_coords(self):
        min_x = min(self.corners, key=lambda c: c[0])[0]
        max_x = max(self.corners, key=lambda c: c[0])[0]
        min_y = min(self.corners, key=lambda c: c[1])[1]
        max_y = max(self.corners, key=lambda c: c[1])[1]
        all_coords = []
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                all_coords.append((x, y))
        return all_coords

    def get_z_addition(self):
        return abs(self.corners[0][2] - self.corners[1][2]) + 1


def parse_input():
    blocks = []
    with open("data.txt") as data_file:
        next_name = 1
        for line in data_file:
            str_coords = line.strip().split("~")
            corners = [[int(c) for c in coord.split(",")] for coord in str_coords]
            min_z = min(corners, key=lambda c: c[2])[2]
            heappush(blocks, (min_z, next_name, Block(next_name, corners)))
            next_name += 1
    return blocks


def solve(part1: bool):
    blocks = parse_input()
    copied_blocks = []
    total_blocks = len(blocks)

    curr_height = defaultdict(lambda: (0, None))
    support_count_by_block_name = defaultdict(int)
    blocks_supported_by_input = defaultdict(set)
    which_blocks_support_me = defaultdict(set)
    while blocks:
        _, _, block = heappop(blocks)
        copied_blocks.append(block)
        max_curr_height = 0
        for coord in block.get_x_y_coords():
            max_curr_height = max(max_curr_height, curr_height[coord][0])

        final_coords = []
        for coord in block.get_x_y_coords():
            if curr_height[coord][0] == max_curr_height:
                supporting_block_name = curr_height[coord][1]
                if supporting_block_name:
                    which_blocks_support_me[block.name].add(supporting_block_name)
                if (
                    supporting_block_name
                    and block.name
                    not in blocks_supported_by_input[supporting_block_name]
                ):
                    blocks_supported_by_input[supporting_block_name].add(block.name)
                    support_count_by_block_name[block.name] += 1

            curr_height[coord] = (max_curr_height + block.get_z_addition(), block.name)
            for z in range(
                max_curr_height + 1, max_curr_height + block.get_z_addition() + 1
            ):
                final_coords.append((coord[0], coord[1], z))

    # part 1
    if part1:
        removable_count = 0
        for block_name in range(1, total_blocks + 1):
            can_remove = True
            for supported_block_name in blocks_supported_by_input[block_name]:
                if support_count_by_block_name[supported_block_name] == 1:
                    can_remove = False
                    break
            if can_remove:
                removable_count += 1
        return removable_count

    # part 2
    total_to_fall = 0
    for block in copied_blocks:
        have_fallen = set()
        to_evaluate = [block.name]
        while to_evaluate:
            curr_block = to_evaluate.pop(0)
            if curr_block in have_fallen:
                continue
            have_fallen.add(curr_block)
            total_to_fall += 1

            for supported_block_name in blocks_supported_by_input[curr_block]:
                if supported_block_name not in have_fallen and which_blocks_support_me[
                    supported_block_name
                ].issubset(have_fallen):
                    to_evaluate.append(supported_block_name)

    # subtract the blocks that have disintegrated, since I counted them as falling above
    return total_to_fall - total_blocks


def part1():
    return solve(part1=True)


def part2():
    return solve(part1=False)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
