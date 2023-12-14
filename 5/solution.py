from dataclasses import dataclass


def get_min_seed_location() -> int:
    min_seed_location = -1
    current_map = {}
    with open("data.txt") as data_file:
        line_num = 0
        for line in data_file:
            if line_num == 0:
                print(line)
                seeds = line.split(" ")[1:]
                for i in range(int(len(seeds) / 2)):
                    seed = int(seeds[i * 2])
                    seed_range = int(seeds[i * 2 + 1])
                    current_map[(seed, seed_range)] = None
                print(f"Start current_map {current_map} \n")
            elif line == "\n":
                new_map = {}
                for (start, range_len), value in current_map.items():
                    if value is not None:
                        new_map[(value, range_len)] = None
                    else:
                        new_map[(start, range_len)] = None
                current_map = new_map
                print(f"New current_map {current_map} \n\n")
            elif line[0].isdigit():
                [dest_start, source_start, range_len] = [
                    int(num) for num in line.split(" ")
                ]
                print(
                    f"Dest start {dest_start}, source start {source_start}, range len {range_len}"
                )
                for seed_start, seed_range_len in list(current_map.keys()):
                    overlapping_range = calculate_overlapping_ranges(
                        seed_start,
                        seed_start + seed_range_len - 1,
                        source_start,
                        source_start + range_len - 1,
                    )
                    print(f"Start {seed_start}, range_len {seed_range_len}")
                    print(f"Overlapping range {overlapping_range}")

                    if overlapping_range.overlapping_range is not None:
                        if overlapping_range.non_valid_ranges:
                            del current_map[(seed_start, seed_range_len)]

                        overlap_start, overlap_range_len = (
                            overlapping_range.overlapping_range[0],
                            overlapping_range.overlapping_range[1]
                            - overlapping_range.overlapping_range[0]
                            + 1,
                        )
                        current_map[(overlap_start, overlap_range_len)] = dest_start + (
                            overlap_start - source_start
                        )
                        for non_valid_range in overlapping_range.non_valid_ranges:
                            non_valid_range_start, non_valid_range_len = (
                                non_valid_range[0],
                                non_valid_range[1] - non_valid_range[0] + 1,
                            )
                            current_map[
                                (non_valid_range_start, non_valid_range_len)
                            ] = None
                print(f"current_map {current_map}\n")

            line_num += 1

        print(f"Final current_map {current_map}")
        for (start, range_len), value in current_map.items():
            location = start if value is None else value
            min_seed_location = (
                location
                if min_seed_location == -1 or location < min_seed_location
                else min_seed_location
            )

    return min_seed_location


@dataclass
class OverlappingRange:
    overlapping_range: tuple
    non_valid_ranges: list[tuple]


def calculate_overlapping_ranges(
    seed_start, seed_end, map_start, map_end
) -> OverlappingRange:
    print(
        f"Seed start {seed_start}, seed end {seed_end} || Map start {map_start}, map end {map_end}"
    )
    overlapping_range = None
    non_valid_ranges = []
    if seed_start >= map_start and seed_start <= map_end:
        if seed_end <= map_end:
            overlapping_range = (seed_start, seed_end)
        else:
            overlapping_range = (seed_start, map_end)
            non_valid_ranges.append((map_end + 1, seed_end))
    elif seed_end >= map_start and seed_end <= map_end:
        overlapping_range = (map_start, seed_end)
        non_valid_ranges.append((seed_start, map_start - 1))
    elif seed_start < map_start and seed_end > map_end:
        overlapping_range = (map_start, map_end)
        non_valid_ranges.append((seed_start, map_start - 1))
        non_valid_ranges.append((map_end + 1, seed_end))
    return OverlappingRange(overlapping_range, non_valid_ranges)


if __name__ == "__main__":
    print(get_min_seed_location())
