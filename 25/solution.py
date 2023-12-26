from collections import defaultdict


def parse_input():
    graph = defaultdict(set)
    with open("data.txt") as data_file:
        for line in data_file:
            [start, rest] = line.strip().split(":")
            connected_nodes = rest.split(" ")
            for node in connected_nodes:
                if node != "":
                    graph[start].add(node)
                    graph[node].add(start)

    return graph


# Pulled this idea from the subreddit, after trying the naive solution and Karger-Stein.
def part1():
    graph = parse_input()
    subgraph_nodes = set(graph)

    def count(node):
        return len(graph[node] - subgraph_nodes)

    while sum(map(count, subgraph_nodes)) != 3:
        subgraph_nodes.remove(max(subgraph_nodes, key=count))

    return len(subgraph_nodes) * len(set(graph) - subgraph_nodes)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
