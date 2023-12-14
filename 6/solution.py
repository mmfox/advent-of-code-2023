import math


def get_sufficient_wait_times(total_time, record_distance) -> tuple[int, int]:
    sqrt = math.sqrt(total_time**2 - 4 * record_distance)
    first_sol = (total_time - sqrt) / 2
    second_sol = (total_time + sqrt) / 2
    return (first_sol, second_sol)


def solution():
    product = 1
    with open("data.txt") as data_file:
        time_to_record = []
        for line in data_file:
            new_line = line.replace(" ", "").replace("\n", "")
            nums = [int(num) for num in new_line.split(":") if num.isdigit()]
            if time_to_record == []:
                for num in nums:
                    time_to_record.append([num])
            else:
                for i in range(len(nums)):
                    time_to_record[i].append(nums[i])

        for [time, record] in time_to_record:
            (min_time, max_time) = get_sufficient_wait_times(time, record)
            rounded_min_time = math.ceil(min_time)
            rounded_max_time = math.floor(max_time)
            num_possible_times = rounded_max_time - rounded_min_time + 1
            if min_time == rounded_min_time:
                num_possible_times -= 1
            if max_time == rounded_max_time:
                num_possible_times -= 1

            if num_possible_times <= 0:
                product = 0
            else:
                product *= num_possible_times
    return product


if __name__ == "__main__":
    print(f"Result is {solution()}")
