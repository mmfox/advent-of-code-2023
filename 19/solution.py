from dataclasses import dataclass
from functools import reduce
import re


@dataclass
class Check:
    field: str
    less_than: bool
    value: int
    next_rule: str


@dataclass
class Rule:
    name: str
    checks: list[Check]
    default_next_rule: str

    def next_rule(self, part: dict[str, int]):
        for check in self.checks:
            if check.less_than:
                if part[check.field] < check.value:
                    return check.next_rule
            else:
                if part[check.field] > check.value:
                    return check.next_rule
        return self.default_next_rule


def parse_input():
    rule_dict = {}
    parts = []
    with open("data.txt") as data_file:
        for line in data_file:
            if line[0].isalpha():
                match = re.match(r"(\w+)\{(.*)\}", line)
                rule_name = match.group(1)
                checks = []
                default_next_rule = None
                for check in match.group(2).split(","):
                    if ":" not in check:
                        default_next_rule = check
                        break
                    [val, next_rule] = check[2:].split(":")
                    checks.append(
                        Check(
                            field=check[0],
                            less_than=check[1] == "<",
                            value=int(val),
                            next_rule=next_rule,
                        )
                    )
                rule_dict[rule_name] = Rule(rule_name, checks, default_next_rule)
            elif line[0] == "{":
                match = re.match(r"\{(.*)\}", line)
                parts.append(
                    {
                        field: int(value)
                        for field, value in (
                            part.split("=") for part in match.group(1).split(",")
                        )
                    }
                )

    return rule_dict, parts


def part1():
    total_sum = 0
    rule_dict, parts = parse_input()
    for part in parts:
        curr_rule = "in"
        while curr_rule not in ("A", "R"):
            curr_rule = rule_dict[curr_rule].next_rule(part)
        if curr_rule == "A":
            for value in part.values():
                total_sum += value
    return total_sum


@dataclass
class ConstrainedPart:
    properties: dict[str, tuple[int, int]]
    next_rule: str

    def calculate_possibilities(self):
        return reduce(
            lambda x, y: x * y, (y - x + 1 for x, y in self.properties.values())
        )


def part2():
    count = 0
    rule_dict, _ = parse_input()
    constrained_part = ConstrainedPart(
        properties={"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)},
        next_rule="in",
    )
    to_explore = [constrained_part]
    while to_explore:
        curr_part = to_explore.pop()
        if curr_part.next_rule == "A":
            count += curr_part.calculate_possibilities()
        elif curr_part.next_rule == "R":
            continue
        else:
            rule = rule_dict[curr_part.next_rule]
            for check in rule.checks:
                if check.less_than:
                    if curr_part.properties[check.field][0] < check.value:
                        new_properties = curr_part.properties.copy()
                        new_properties[check.field] = (
                            new_properties[check.field][0],
                            min(check.value - 1, new_properties[check.field][1]),
                        )
                        to_explore.append(
                            ConstrainedPart(new_properties, check.next_rule)
                        )
                    if curr_part.properties[check.field][1] >= check.value:
                        curr_part.properties[check.field] = (
                            max(curr_part.properties[check.field][0], check.value),
                            curr_part.properties[check.field][1],
                        )
                    else:
                        curr_part = None
                        break
                else:
                    if curr_part.properties[check.field][1] > check.value:
                        new_properties = curr_part.properties.copy()
                        new_properties[check.field] = (
                            max(check.value + 1, new_properties[check.field][0]),
                            curr_part.properties[check.field][1],
                        )
                        to_explore.append(
                            ConstrainedPart(new_properties, check.next_rule)
                        )
                    if curr_part.properties[check.field][0] <= check.value:
                        curr_part.properties[check.field] = (
                            curr_part.properties[check.field][0],
                            min(curr_part.properties[check.field][1], check.value),
                        )
                    else:
                        curr_part = None
                        break

            if curr_part is not None:
                to_explore.append(
                    ConstrainedPart(curr_part.properties, rule.default_next_rule)
                )

    return count


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
