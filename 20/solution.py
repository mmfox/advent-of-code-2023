from collections import defaultdict
import math


class Node:
    def __init__(self, name, neighbors):
        self.name = name
        self.neighbors = neighbors
        self.state = False

    def get_state(self):
        return (self.state,)

    def process_signal(
        self, sending_node: str, signal: bool
    ) -> list[tuple[str, str, bool]]:
        raise NotImplementedError("Must implement process_signal")


class Broadcaster(Node):
    def process_signal(
        self, sending_node: str, signal: bool
    ) -> list[tuple[str, str, bool]]:
        self.state = signal
        return [(self.name, neighbor, signal) for neighbor in self.neighbors]


class FlipFlop(Node):
    def __init__(self, name, neighbors):
        super().__init__(name, neighbors)

    def process_signal(
        self, sending_node: str, signal: bool
    ) -> list[tuple[str, str, bool]]:
        if not signal:
            self.state = not self.state
            return [(self.name, neighbor, self.state) for neighbor in self.neighbors]
        else:
            return []


class Conjunction(Node):
    def __init__(self, name, neighbors):
        super().__init__(name, neighbors)
        self.input_state = {}
        self.state = True

    def get_state(self):
        return (self.state, dict(self.input_state))

    def setup_input_state(self, name: str):
        self.input_state[name] = False

    def process_signal(
        self, sending_node: str, signal: bool
    ) -> list[tuple[str, str, bool]]:
        self.input_state[sending_node] = signal
        if all(self.input_state.values()):
            self.state = False
            return [(self.name, neighbor, self.state) for neighbor in self.neighbors]
        else:
            self.state = True
            return [(self.name, neighbor, self.state) for neighbor in self.neighbors]


class Graph:
    def __init__(self):
        self.nodes = {}
        self.inputs_by_node = defaultdict(list)
        self.conjunctions = []

    def add_node(self, node: Node):
        if isinstance(node, Conjunction):
            self.conjunctions.append(node.name)
        self.nodes[node.name] = node
        for neighbor in node.neighbors:
            self.inputs_by_node[neighbor].append(node.name)

    def setup_conjunctions(self):
        for conj in self.conjunctions:
            for input_node in self.inputs_by_node[conj]:
                conj_node = self.nodes[conj]
                conj_node.setup_input_state(input_node)

    def send_signal(self) -> tuple[int, int, bool]:
        low_count = 1
        high_count = 0
        to_process = [("button", "broadcaster", False)]
        sent_relevant_signal = set()
        while to_process:
            sending_node, receiving_node, signal = to_process.pop(0)
            if receiving_node in self.inputs_by_node["rx"] and signal:
                sent_relevant_signal.add(sending_node)
            if receiving_node not in self.nodes:
                continue
            new_signals = self.nodes[receiving_node].process_signal(
                sending_node, signal
            )
            for new_signal in new_signals:
                if new_signal[2]:
                    high_count += 1
                else:
                    low_count += 1
            to_process.extend(new_signals)

        return low_count, high_count, sent_relevant_signal

    def get_state(self):
        return {name: node.get_state() for name, node in self.nodes.items()}


def parse_neighbors(params):
    neighbors = []
    for param in params[2:]:
        if param[-1] == ",":
            param = param[:-1]
        neighbors.append(param)
    return neighbors


def parse_input():
    graph = Graph()
    with open("data.txt") as data_file:
        for line in data_file:
            params = line.strip().split(" ")
            if params[0] == "broadcaster":
                node = Broadcaster(params[0], parse_neighbors(params))
            elif params[0][0] == "%":
                name = params[0][1:]
                node = FlipFlop(name, parse_neighbors(params))
            elif params[0][0] == "&":
                name = params[0][1:]
                node = Conjunction(name, parse_neighbors(params))
            else:
                raise ValueError(f"Invalid node type: {params[0]}")

            graph.add_node(node)
    return graph


def send_pulses(total_iterations=1000):
    graph = parse_input()
    graph.setup_conjunctions()
    initial_state = graph.get_state()
    low_pulse_counts = []
    high_pulse_counts = []

    curr_state = None

    cycle_tracker = {}
    button_presses = 0
    while curr_state != initial_state and button_presses < total_iterations:
        button_presses += 1
        low_count, high_count, sent_relevant_signal = graph.send_signal()
        low_pulse_counts.append(low_count)
        high_pulse_counts.append(high_count)
        curr_state = graph.get_state()
        for node in sent_relevant_signal:
            if node not in cycle_tracker:
                cycle_tracker[node] = button_presses

    # Part 2:
    rx_cycles = math.lcm(*cycle_tracker.values())

    if button_presses == total_iterations:
        return sum(low_pulse_counts) * sum(high_pulse_counts), rx_cycles

    cycle_iterations = button_presses
    remainder = total_iterations % cycle_iterations
    cycles = total_iterations // cycle_iterations

    low_count = cycles * sum(low_pulse_counts) + sum(low_pulse_counts[:remainder])
    high_count = cycles * sum(high_pulse_counts) + sum(high_pulse_counts[:remainder])
    print(f"Low count: {low_count}, High count: {high_count}")
    print(f"Cycles: {cycles}, Remainder: {remainder}")

    return low_count * high_count, rx_cycles


def part1():
    product, _ = send_pulses(total_iterations=1000)
    return product


def part2():
    _, rx_cycles = send_pulses(total_iterations=5000)
    return rx_cycles


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
