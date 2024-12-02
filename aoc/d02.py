from aoc.helpers import *
from copy import deepcopy
from typing import Iterator
from itertools import pairwise


def parse(input: str) -> list[list[int]]:
    return [[int(level) for level in line.split()] for line in input.splitlines()]


def get_diffs(report: list[int]) -> list[int]:
    return [pair[1] - pair[0] for pair in pairwise(report)]


def is_safe(report: list[int]) -> bool:
    diffs = get_diffs(report)
    return all(map(lambda diff: abs(diff) >= 1 and abs(diff) <= 3, diffs)) and (
        all(map(lambda diff: diff > 0, diffs)) or all(map(lambda diff: diff < 0, diffs))
    )


def p1(reports: list[list[int]]) -> int:
    return len(list(filter(is_safe, reports)))


def variants_without_one_level(report: list[int]) -> Iterator[list[int]]:
    for idx in range(len(report)):
        variant = deepcopy(report)
        del variant[idx]
        yield variant


def is_safe_p2(report: list[int]) -> bool:
    return is_safe(report) or any(map(is_safe, variants_without_one_level(report)))


def p2(reports: list[list[int]]) -> int:
    return len(list(filter(is_safe_p2, reports)))


if __name__ == "__main__":
    reports = read_input("d02", parser=parse)

    p1_ans = p1(reports)
    assert p1_ans == 502
    print(f"p1: {p1_ans}")

    p2_ans = p2(reports)
    assert p2_ans == 544
    print(f"p2: {p2_ans}")


def test_p1():
    test_reports = read_test_input("d02", parser=parse)
    assert p1(test_reports) == 2


def test_p2():
    test_reports = read_test_input("d02", parser=parse)
    assert p2(test_reports) == 4
