from aoc.helpers import *
from typing import Optional
from dataclasses import dataclass
from collections import defaultdict
from itertools import combinations
from functools import reduce


@dataclass
class Map:
    antennas: dict[str, list[tuple[int, int]]]
    max_row: int
    max_col: int

    def all_antinodes(self, part2: bool = False) -> set[tuple[int, int]]:
        return reduce(lambda acc, elem: acc.union(self.antinodes(elem, part2)), self.antennas.keys(), set())

    def antinodes(self, frequency: str, part2: bool = False) -> set[tuple[int, int]]:
        """Returns all antinodes for the antennas with `frequency`."""
        match self.antennas.get(frequency):
            case None:
                return []
            case antennas:
                res = set()
                for a1, a2 in combinations(antennas, 2):
                    res = res.union(self._antinodes_for_pair(a1, a2, max_k=None if part2 else 1))
                return res

    def is_inside(self, c: tuple[int, int]) -> bool:
        return c[0] >= 0 and c[0] <= self.max_row and c[1] >= 0 and c[1] <= self.max_col

    def _antinodes_for_pair(
        self, a1: tuple[int, int], a2: tuple[int, int], max_k: Optional[int] = None
    ) -> set[tuple[int, int]]:
        res = {a1, a2} if max_k is None else set()
        drow, dcol = a2[0] - a1[0], a2[1] - a1[1]
        for origin, direction in [(a1, -1), (a2, 1)]:
            k = 1
            while max_k is None or k <= max_k:
                node = (origin[0] + direction * k * drow, origin[1] + direction * k * dcol)
                if self.is_inside(node):
                    res.add(node)
                    k += 1
                else:
                    break
        return res


def parse(input: str) -> Map:
    antennas, max_row, max_col = defaultdict(list), 0, 0

    for row_idx, row in enumerate(input.splitlines()):
        for col_idx, ch in enumerate(row):
            if ch != ".":
                antennas[ch].append((row_idx, col_idx))
            max_col = max(max_col, col_idx)
        max_row = max(max_row, row_idx)

    return Map(antennas=antennas, max_row=max_row, max_col=max_col)


def p1(input: Map) -> int:
    return len(input.all_antinodes())


def p2(input: Map) -> int:
    return len(input.all_antinodes(part2=True))


if __name__ == "__main__":
    input = read_input("d08", parser=parse)

    p1_ans = p1(input)
    assert p1_ans == 381
    print(f"p1: {p1_ans}")

    p2_ans = p2(input)
    assert p2_ans == 1184
    print(f"p2: {p2_ans}")


def test_p1():
    input = read_test_input("d08", parser=parse)
    assert p1(input) == 14


def test_p2():
    input = read_test_input("d08", parser=parse)
    assert p2(input) == 34
