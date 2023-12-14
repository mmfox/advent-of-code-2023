from functools import cache


def is_valid_run(line, counts):
    runs = [run for run in line.split(".") if run != ""]
    if len(runs) != len(counts):
        return False
    for i, run in enumerate(runs):
        if len(run) != counts[i]:
            return False
    return True


def calculate_num_alt_configs(line):
    record, counts = line.strip().split(" ")
    counts = [int(count) for count in counts.split(",")]
    num_wildcards = record.count("?")
    num_configurations = 0
    for i in range(2**num_wildcards):
        binary = bin(i)[2:]
        binary = "0" * (num_wildcards - len(binary)) + binary
        new_record = record
        for j, char in enumerate(binary):
            to_use = "." if char == "0" else "#"
            new_record = new_record.replace("?", to_use, 1)
        if is_valid_run(new_record, counts):
            num_configurations += 1
    return num_configurations


def part1():
    total_configurations = 0
    with open("data.txt") as data_file:
        for line in data_file:
            total_configurations += calculate_num_alt_configs(line)
    return total_configurations


def part2():
    @cache
    def recurse(record, counts):
        curr_size = 0
        all_sizes = []
        last_dot_index = 0

        for i in range(len(record)):
            if record[i] == ".":
                last_dot_index = i
                if curr_size > 0:
                    all_sizes.append(curr_size)
                    if tuple(all_sizes) != counts[: len(all_sizes)]:
                        return 0
                    curr_size = 0
            elif record[i] == "#":
                curr_size += 1
            else:
                return recurse(
                    record[last_dot_index:i] + "." + record[i + 1 :],
                    counts[len(all_sizes) :],
                ) + recurse(
                    record[last_dot_index:i] + "#" + record[i + 1 :],
                    counts[len(all_sizes) :],
                )

        if curr_size > 0:
            all_sizes.append(curr_size)

        return 1 if tuple(all_sizes) == counts else 0

    total_configs = 0
    with open("data.txt") as data_file:
        for line in data_file:
            record, line_counts = line.strip().split(" ")
            new_record = "?".join([record] * 5)
            new_counts = ",".join([line_counts] * 5)
            final_counts = tuple(int(c) for c in new_counts.split(","))
            total_configs += recurse(new_record, final_counts)
    return total_configs


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
