from dataclasses import dataclass
import re
from typing import Optional


@dataclass
class HailStone:
    x: int
    y: int
    z: int
    dx: int
    dy: int
    dz: int

    @property
    def xy_slope(self):
        return self.dy / self.dx

    @property
    def y_intercept(self):
        return self.y - self.xy_slope * self.x


def is_point_in_future(hs: HailStone, pos: tuple[int, int]) -> bool:
    x, y = pos
    if (hs.dx < 0 and x > hs.x) or (hs.dx > 0 and x < hs.x):
        return False
    elif (hs.dy < 0 and y > hs.y) or (hs.dy > 0 and y < hs.y):
        return False

    return True


def calculate_xy_collision(hs1: HailStone, hs2: HailStone) -> Optional[tuple[int, int]]:
    if hs1.xy_slope == hs2.xy_slope:
        return None
    x = (hs2.y_intercept - hs1.y_intercept) / (hs1.xy_slope - hs2.xy_slope)
    y = hs1.xy_slope * x + hs1.y_intercept
    return (x, y)


def parse_input():
    hail = []
    with open("data.txt") as data_file:
        for line in data_file:
            res = re.findall("\-?\d+", line.strip())
            hail.append(HailStone(*map(int, res)))
    return hail


def part1(min_col: int, max_col: int):
    count = 0
    hail = parse_input()
    for i in range(len(hail)):
        for j in range(i + 1, len(hail)):
            collision = calculate_xy_collision(hail[i], hail[j])
            if collision is not None:
                x, y = collision
                if (
                    min_col <= x <= max_col
                    and min_col <= y <= max_col
                    and is_point_in_future(hail[i], collision)
                    and is_point_in_future(hail[j], collision)
                ):
                    count += 1
    return count


# Skipping part 2 today because it's not the kind of problem I enjoy solving.
def part2():
    pass


if __name__ == "__main__":
    print(f"Part 1: {part1(200000000000000, 400000000000000)}")
    print(f"Part 2: {part2()}")
