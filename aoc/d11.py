from aoc.helpers import *
import math


def parse(input: str) -> list[int]:
    return [int(stone) for stone in input.splitlines()[0].split()]


def run(stone: int, remaining_blinks: int, memo: dict[tuple[int, int], int]):
    from_memo = memo.get((stone, remaining_blinks))
    if from_memo:
        return from_memo
    elif remaining_blinks == 0:
        return 1
    elif stone == 0:
        res = run(1, remaining_blinks - 1, memo)
        memo[(stone, remaining_blinks)] = res
        return res
    elif math.log10(stone) >= 1.0 and math.floor(math.log10(stone)) % 2 == 1:
        digits = str(stone)
        first, second = int(digits[: len(digits) // 2]), int(digits[len(digits) // 2 :])
        res = run(first, remaining_blinks - 1, memo) + run(second, remaining_blinks - 1, memo)
        memo[(stone, remaining_blinks)] = res
        return res
    else:
        res = run(stone * 2024, remaining_blinks - 1, memo)
        memo[(stone, remaining_blinks)] = res
        return res


def p1(stones: list[int]) -> int:
    memo = {}
    return sum([run(stone, 25, memo) for stone in stones])


def p2(stones: list[int]) -> int:
    memo = {}
    return sum([run(stone, 75, memo) for stone in stones])


if __name__ == "__main__":
    input = read_input("d11", parser=parse)

    p1_ans = p1(input)
    assert p1_ans == 218079
    print(f"p1: {p1_ans}")

    p2_ans = p2(input)
    assert p2_ans == 259755538429618
    print(f"p2: {p2_ans}")


def test_p1():
    input = read_test_input("d11", parser=parse)
    assert p1(input) == 55312
