from aoc.helpers import *

TARGET = "XMAS"
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]


def parse(input: str) -> list[list[str]]:
    return [list(row) for row in input.splitlines()]


def p1(input: list[list[str]]) -> int:
    """
    Walks in all directions from each "X" it finds and counts matches.
    """
    found, max_row, max_col = 0, len(input), len(input[0])
    for row in range(max_row):
        for col in range(max_col):
            if input[row][col] == TARGET[0]:
                for drow, dcol in DIRECTIONS:
                    matches = [
                        input[row + drow * offset][col + dcol * offset] == TARGET[offset]
                        for offset in range(1, len(TARGET))
                        if row + drow * offset >= 0
                        and col + dcol * offset >= 0
                        and row + drow * offset < max_row
                        and col + dcol * offset < max_col
                    ]
                    if len(matches) == len(TARGET) - 1 and all(matches):
                        found += 1
    return found


X_POS = [[(-1, -1), (1, 1)], [(-1, 1), (1, -1)]]


def p2(input: list[list[str]]) -> int:
    """
    Walks both diagonal sides from each "A" it finds and checks that sides match "M(A)S" or "S(A)M".
    """
    found, max_row, max_col = 0, len(input), len(input[0])
    for row in range(max_row):
        for col in range(max_col):
            if input[row][col] == "A":
                is_match = True
                for side in X_POS:
                    around = [
                        input[row + drow][col + dcol]
                        for drow, dcol in side
                        if row + drow >= 0 and row + drow < max_row and col + dcol >= 0 and col + dcol < max_col
                    ]
                    is_match = is_match and (around == ["M", "S"] or around == ["S", "M"])
                if is_match:
                    found += 1
    return found


if __name__ == "__main__":
    input = read_input("d04", parser=parse)

    p1_ans = p1(input)
    assert p1_ans == 2378
    print(f"p1: {p1_ans}")

    p2_ans = p2(input)
    assert p2_ans == 1796
    print(f"p2: {p2_ans}")


def test_p1():
    input = read_test_input("d04", parser=parse)
    assert p1(input) == 18


def test_p2():
    input = read_test_input("d04", parser=parse)
    assert p2(input) == 9
