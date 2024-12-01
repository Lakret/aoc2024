from collections import Counter
from aoc.helpers import *


def parse(input: str) -> tuple[list[int], list[int]]:
    left, right = [], []
    for line in input.splitlines():
        match line.split():
            case [l, r]:
                left.append(int(l))
                right.append(int(r))
    return (left, right)


def p1(left: list[int], right: list[int]) -> int:
    left.sort()
    right.sort()
    return sum([abs(l - r) for (l, r) in zip(left, right)])


def p2(left: list[int], right: list[int]) -> int:
    frequencies = Counter(right)
    return sum([id * frequencies[id] for id in left])


if __name__ == "__main__":
    (left, right) = read_input("d01", parser=parse)

    p1_ans = p1(left, right)
    assert p1_ans == 1151792
    print(f"p1: {p1_ans}")

    p2_ans = p2(left, right)
    assert p2_ans == 21790168
    print(f"p2: {p2_ans}")


def test_p1():
    (left, right) = read_test_input("d01", parser=parse)
    assert p1(left, right) == 11


def test_p2():
    (left, right) = read_test_input("d01", parser=parse)
    assert p2(left, right) == 31
