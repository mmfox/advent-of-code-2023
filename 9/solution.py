def should_continue(nums: list[int]) -> bool:
    key = nums[0]
    for num in nums:
        if num != key:
            return True
    return False


def solution():
    total_sum = 0
    with open("data.txt") as data_file:
        stack = []

        for line in data_file:
            nums = [int(num) for num in line.split()]
            stack.append(nums[0])
            while should_continue(nums):
                nums = [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]
                stack.append(nums[0])

            to_sub = stack.pop()
            while stack:
                to_sub = stack.pop() - to_sub

            total_sum += to_sub

    return total_sum


if __name__ == "__main__":
    print(solution())
