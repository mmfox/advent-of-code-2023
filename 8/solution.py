import math
import re


def should_continue(curr_nodes: list[str]) -> bool:
    for node in curr_nodes:
        if node[-1] != "Z":
            return True
    return False


def solution():
    with open("data.txt") as data_file:
        data = data_file.read().splitlines()
        instructions = data[0]
        graph = {}
        curr_nodes = []
        for connection in data[2:]:
            match = re.match("(\w+) = \((\w+), (\w+)\)", connection)
            start, left, right = match.groups()
            if start[-1] == "A":
                curr_nodes.append(start)
            graph[start] = (left, right)

        # while should_continue(curr_nodes):
        #    instruction = instructions[instruction_index]
        #    next_nodes = []
        #    for curr_node in curr_nodes:
        #        if instruction == "L":
        #            next_nodes.append(graph[curr_node][0])
        #        elif instruction == "R":
        #            next_nodes.append(graph[curr_node][1])
        #    curr_nodes = next_nodes
        #    instruction_index = (instruction_index + 1) % len(instructions)
        #    num_hops += 1

        hops = []
        for node in curr_nodes:
            curr_node = node
            visited = set()
            instruction_index = 0
            num_hops = 0
            while True:
                instruction = instructions[instruction_index]
                if instruction == "L":
                    curr_node = graph[curr_node][0]
                elif instruction == "R":
                    curr_node = graph[curr_node][1]
                instruction_index = (instruction_index + 1) % len(instructions)
                num_hops += 1
                if curr_node[-1] == "Z":
                    break
            hops.append(num_hops)
        print(hops)

    return math.lcm(*hops)


if __name__ == "__main__":
    print(solution())
