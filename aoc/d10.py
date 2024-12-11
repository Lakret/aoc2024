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


def score_trailhead_reachable_summits(m: Map, coords: tuple[int, int]) -> int:
    stack, summits = [coords], set()
    while stack:
        (row, col) = pos = stack.pop()
        for drow, dcol in DIRECTIONS:
            new_pos = (row + drow, col + dcol)
            new_height = m.grid.get(new_pos)
            if new_height and new_height == m.grid[pos] + 1:
                if new_height == 9:
                    summits.add(new_pos)
                else:
                    stack.append(new_pos)
    return len(summits)


def p1(m: Map) -> int:
    return sum([score_trailhead_reachable_summits(m, th) for th in m.trailheads()])


def score_trailhead_distinct_trails(m: Map, coords: tuple[int, int]) -> int:
    stack, score = [coords], 0
    while stack:
        (row, col) = pos = stack.pop()
        for drow, dcol in DIRECTIONS:
            new_pos = (row + drow, col + dcol)
            new_height = m.grid.get(new_pos)
            if new_height and new_height == m.grid[pos] + 1:
                if new_height == 9:
                    score += 1
                else:
                    stack.append(new_pos)
    return score


def p2(m: Map) -> int:
    return sum([score_trailhead_distinct_trails(m, th) for th in m.trailheads()])


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
