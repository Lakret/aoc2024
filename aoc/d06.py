from aoc.helpers import *
from collections import defaultdict
from dataclasses import dataclass, replace


TURNS = {(-1, 0): (0, 1), (0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0)}


@dataclass
class State:
    obstacles: set[(int, int)]
    pos: tuple[int, int]
    direction: tuple[int, int]
    max_row: int
    max_col: int

    def walk(self) -> "State":
        new_pos = self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]
        if new_pos in self.obstacles:
            return replace(self, direction=TURNS[self.direction])
        else:
            return replace(self, pos=new_pos)

    def walk_to_exit(self) -> set[tuple[int, int]]:
        """Returns a set of visited positions"""
        visited, state = set(), replace(self)
        while state.inside():
            visited.add(state.pos)
            state = state.walk()
        return visited

    def inside(self) -> bool:
        return self.pos[0] <= self.max_row and self.pos[1] <= self.max_col and self.pos[0] >= 0 and self.pos[1] >= 0


def parse(input: str) -> State:
    obstacles, pos, direction, max_row, max_col = set(), None, None, 0, 0
    for row_idx, row in enumerate(input.splitlines()):
        for col_idx, ch in enumerate(row):
            match ch:
                case ".":
                    continue
                case "#":
                    obstacles.add((row_idx, col_idx))
                case _:
                    pos = (row_idx, col_idx)
                    match ch:
                        case "^":
                            direction = (-1, 0)
                        case "v":
                            direction = (1, 0)
                        case ">":
                            direction = (0, 1)
                        case "<":
                            direction = (0, -1)
            max_row = max(max_row, row_idx)
            max_col = max(max_col, col_idx)
    return State(obstacles=obstacles, pos=pos, direction=direction, max_row=max_row, max_col=max_col)


def p1(state: State) -> int:
    return len(state.walk_to_exit())


def is_loop(state: State) -> bool:
    # we need to track guard's direction this time to detect loops, and we need to support guard
    # visiting the same cell while walking in different directions, thus we're using set for values
    visited = defaultdict(set)
    visited[state.pos] = {state.direction}
    while state.inside():
        state = state.walk()
        # we arrived at the same point with the same direction for the second time - cycle found
        if visited.get(state.pos) and state.direction in visited[state.pos]:
            return True
        else:
            visited[state.pos].add(state.direction)
    return False


def p2(state: State) -> int:
    # it'll take to long to check all possible position, but we have a natural optimization:
    # just check placing obstacles on the guard's original path only
    states = [
        replace(state, obstacles={obstacle_pos, *state.obstacles})
        for obstacle_pos in state.walk_to_exit()
        if obstacle_pos not in state.obstacles and obstacle_pos != state.pos
    ]
    return len(list(filter(is_loop, states)))


if __name__ == "__main__":
    input = read_input("d06", parser=parse)

    p1_ans = p1(input)
    assert p1_ans == 4665
    print(f"p1: {p1_ans}")

    p2_ans = p2(input)
    assert p2_ans == 1688
    print(f"p2: {p2_ans}")


def test_p1():
    input = read_test_input("d06", parser=parse)
    assert p1(input) == 41


def test_p2():
    input = read_test_input("d06", parser=parse)
    assert p2(input) == 6


def test_is_loop_detects_loops_in_all_test_positions():
    input = read_test_input("d06", parser=parse)
    pos = [(6, 3), (7, 6), (7, 7), (8, 1), (8, 3), (9, 7)]
    assert all([is_loop(replace(input, obstacles={new_obstacle_pos, *input.obstacles})) for new_obstacle_pos in pos])