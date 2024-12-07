from aoc.helpers import *
from copy import deepcopy
from operator import add, mul


def parse(input: str) -> list[tuple[int, list[int]]]:
    res = []
    for equation in input.splitlines():
        match equation.split(": "):
            case [test_value, equation]:
                res.append((int(test_value), [int(v) for v in equation.split()]))
    return res


def is_provable(test_value: int, values: list[int], ops: list[Callable[[int, int], int]] = None):
    ops = ops if ops else [add, mul]
    values = deepcopy(values)
    first = values.pop(0)
    branches, next_branches = [first], []

    while values:
        next_value = values.pop(0)
        for branch in branches:
            for op in ops:
                res = op(branch, next_value)
                next_branches.append(res)
        branches = next_branches
        next_branches = []

    return test_value in branches


def p1(input: list[tuple[int, list[int]]]) -> int:
    return sum([test_value for (test_value, values) in input if is_provable(test_value, values)])


def concat(x: int, y: int) -> int:
    return int(str(x) + str(y))


def p2(input: list[tuple[int, list[int]]]) -> int:
    return sum(
        [test_value for (test_value, values) in input if is_provable(test_value, values, ops=[add, mul, concat])]
    )


if __name__ == "__main__":
    input = read_input("d07", parser=parse)

    p1_ans = p1(input)
    assert p1_ans == 1153997401072
    print(f"p1: {p1_ans}")

    p2_ans = p2(input)
    assert p2_ans == 97902809384118
    print(f"p2: {p2_ans}")


def test_p1():
    input = read_test_input("d07", parser=parse)
    assert p1(input) == 3749


def test_p2():
    input = read_test_input("d07", parser=parse)
    assert p2(input) == 11387
