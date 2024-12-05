from aoc.helpers import *
from dataclasses import dataclass
from collections import defaultdict
from functools import cmp_to_key
from copy import deepcopy


@dataclass
class SafetyManual:
    before: dict[int, set[int]]
    updates: list[list[int]]


def parse(input: str) -> SafetyManual:
    before = defaultdict(set)
    match input.split("\n\n"):
        case [ordering_rules, updates]:
            for line in ordering_rules.splitlines():
                ordering = [int(x) for x in line.split("|")]
                before[ordering[0]].add(ordering[1])
            updates = [[int(n) for n in u.split(",")] for u in updates.splitlines()]
            return SafetyManual(before, updates)


def is_correct(update: list[int], before: dict[int, set[int]]) -> bool:
    seen = set()
    for page in update:
        conflicts = seen.intersection(before.get(page, set()))
        if len(conflicts) == 0:
            seen.add(page)
        else:
            return False
    return True


def mid(update: list[int]) -> int:
    return update[len(update) // 2]


def p1(input: SafetyManual) -> int:
    res = 0
    for update in input.updates:
        if is_correct(update, input.before):
            res += mid(update)
    return res


def to_correct_order(update: list[int], before: dict[int, set[int]]) -> list[int]:
    def compare(x, y):
        x_before = before[x]
        y_before = before[y]
        if y in x_before:
            return -1
        elif x in y_before:
            return 1
        else:
            return 0

    res = deepcopy(update)
    res.sort(key=cmp_to_key(compare))
    return res


def p2(input: SafetyManual) -> int:
    res = 0
    for u in filter(lambda u: not is_correct(u, input.before), input.updates):
        res += mid(to_correct_order(u, input.before))
    return res


if __name__ == "__main__":
    input = read_input("d05", parser=parse)

    p1_ans = p1(input)
    assert p1_ans == 5248
    print(f"p1: {p1_ans}")

    p2_ans = p2(input)
    assert p2_ans == 4507
    print(f"p2: {p2_ans}")


def test_p1():
    input = read_test_input("d05", parser=parse)
    assert p1(input) == 143


def test_p2():
    input = read_test_input("d05", parser=parse)
    assert p2(input) == 123
