from collections import defaultdict
from webbrowser import get


def part1():
    total_sum = 0
    with open("data.txt") as data_file:
        codes = data_file.readlines()[0].split(",")

    for code in codes:
        total_sum += get_hash(code)
    return total_sum


def get_hash(code):
    hash = 0
    for char in code:
        hash += ord(char)
        hash *= 17
        hash %= 256
    return hash


def get_first_index_of_label(box, label):
    for i, (l, _) in enumerate(box):
        if l == label:
            return i
    return -1


def part2():
    total_sum = 0
    with open("data.txt") as data_file:
        codes = data_file.readlines()[0].split(",")

    boxes = defaultdict(list)
    for code in codes:
        if "=" in code:
            [label, focal_length] = code.split("=")
            hash = get_hash(label)
            first_index = get_first_index_of_label(boxes[hash], label)
            if first_index != -1:
                boxes[hash][first_index] = (label, focal_length)
            else:
                boxes[hash].append((label, focal_length))
        else:
            hash = get_hash(code[:-1])
            first_index = get_first_index_of_label(boxes[hash], code[:-1])
            if first_index != -1:
                boxes[hash].pop(first_index)

    return calculate_focusing_power(boxes)


def calculate_focusing_power(boxes):
    total_sum = 0
    for box_num, lenses in boxes.items():
        for i, (label, focal_length) in enumerate(lenses):
            total_sum += (box_num + 1) * int(focal_length) * (i + 1)
    return total_sum


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 1: {part2()}")
