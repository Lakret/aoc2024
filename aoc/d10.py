from aoc.helpers import *
from dataclasses import dataclass


@dataclass
class Map:
    grid: dict[tuple[int, int], int]
    max_row: int
    max_col: int

    def trailheads(self) -> list[tuple[int, int]]:
        return [coords for (coords, height) in self.grid.items() if height == 0]


def parse(input: str) -> any:
    grid, max_row, max_col = {}, 0, 0

    for row_id, row in enumerate(input.splitlines()):
        for col_id, height in enumerate(row):
            grid[(row_id, col_id)] = int(height)
            max_col = max(col_id, max_col)
        max_row = max(row_id, max_row)

    return Map(grid=grid, max_row=max_row, max_col=max_col)


DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def dfs[
    T
](m: Map, coords: tuple[int, int], score_init: Callable[[], T], score_add: Callable[[T, tuple[int, int]], T]) -> T:
    stack = [coords]
    score = score_init()
    while stack:
        (row, col) = pos = stack.pop()
        for drow, dcol in DIRECTIONS:
            new_pos = (row + drow, col + dcol)
            new_height = m.grid.get(new_pos)
            if new_height and new_height == m.grid[pos] + 1:
                if new_height == 9:
                    score = score_add(score, new_pos)
                else:
                    stack.append(new_pos)
    return score


def p1(m: Map) -> int:
    def score_add(score, new_pos):
        score.add(new_pos)
        return score

    return sum([len(dfs(m, th, set, score_add)) for th in m.trailheads()])


def p2(m: Map) -> int:
    return sum([dfs(m, th, lambda: 0, lambda score, _: score + 1) for th in m.trailheads()])


if __name__ == "__main__":
    input = read_input("d10", parser=parse)

    p1_ans = p1(input)
    assert p1_ans == 786
    print(f"p1: {p1_ans}")

    p2_ans = p2(input)
    assert p2_ans == 1722
    print(f"p2: {p2_ans}")


def test_p1():
    input = read_test_input("d10", parser=parse)
    assert p1(input) == 36


def test_p2():
    input = read_test_input("d10", parser=parse)
    assert p2(input) == 81
