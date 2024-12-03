from aoc.helpers import *
import re

MUL_OPS = r"mul\((?P<x>\d+),(?P<y>\d+)\)"
MUL_IF_OPS = r"mul\((?P<x>\d+),(?P<y>\d+)\)|(?P<do>do\(\))|(?P<dont>don't\(\))"


def p1(input: str) -> int:
    res = 0
    for m in re.finditer(MUL_OPS, input):
        captures = m.groupdict()
        res += int(captures["x"]) * int(captures["y"])
    return res


def p2(input: str) -> int:
    res, on = 0, True

    for m in re.finditer(MUL_IF_OPS, input):
        captures = m.groupdict()
        if captures["do"]:
            on = True
        if captures["dont"]:
            on = False
        if captures["x"] != None and captures["y"] != None and on:
            res += int(captures["x"]) * int(captures["y"])

    return res


if __name__ == "__main__":
    input = read_input("d03")

    p1_ans = p1(input)
    assert p1_ans == 160672468
    print(f"p1: {p1_ans}")

    p2_ans = p2(input)
    assert p2_ans == 84893551
    print(f"p2: {p2_ans}")


def test_p1():
    input = read_test_input("d03")
    assert p1(input) == 161


def test_p2():
    input = read_test_input("d03")
    assert p2(input) == 48
