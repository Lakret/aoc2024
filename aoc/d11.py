from aoc.helpers import *
from copy import deepcopy


def parse(input: str) -> list[int]:
    return [int(stone) for stone in input.splitlines()[0].split()]


def blink(stones: list[any]):
    for pos, stone in enumerate(stones):
        match stone:
            case 0:
                stones[pos] = 1
            case int(num):
                digits = str(num)
                if len(digits) % 2 == 0:
                    stones[pos] = [int(digits[: len(digits) // 2]), int(digits[len(digits) // 2 :])]
                else:
                    stones[pos] *= 2024
            case list(_):
                blink(stone)


def deep_count(stones: list[any]) -> int:
    res = 0
    for stone in stones:
        match stone:
            case int(_):
                res += 1
            case list(substones):
                res += deep_count(substones)
    return res


def p1(stones: list[int]) -> int:
    stones = deepcopy(stones)
    for _ in range(25):
        blink(stones)
    return deep_count(stones)


def p2(stones: list[int]) -> int:
    stones = deepcopy(stones)
    for _ in range(75):
        blink(stones)
    return deep_count(stones)


# TODO: instead of io-list like approach with hybrid list, we can calculate the amount of produced stones
# per each new stone and sum them, that should be faster because we won't need to ever build the whole list


if __name__ == "__main__":
    input = read_input("d11", parser=parse)

    p1_ans = p1(input)
    assert p1_ans == 218079
    print(f"p1: {p1_ans}")

#     p2_ans = p2(input)
#     assert p2_ans == 1722
#     print(f"p2: {p2_ans}")


def test_p1():
    input = read_test_input("d11", parser=parse)
    assert p1(input) == 55312


# def test_p2():
#     input = read_test_input("d10", parser=parse)
#     assert p2(input) == 81
