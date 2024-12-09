from aoc.helpers import *
from dataclasses import dataclass, field
from itertools import repeat


@dataclass
class DiskMap:
    blocks: list[int] = field(default_factory=list)
    free: list[int] = field(default_factory=list)


def parse(input: str) -> DiskMap:
    blocks, free = [], []
    for idx, ch in enumerate(input.strip()):
        if idx % 2 == 0:
            blocks.append(int(ch))
        else:
            free.append(int(ch))
    return DiskMap(blocks=blocks, free=free)


def defrag(dm: DiskMap) -> list[int]:
    res, left_block_id, right_block_id, add_left = [], 0, len(dm.blocks) - 1, True
    right_block_len = dm.blocks[right_block_id]
    free_id, remaining = 0, dm.free[0]

    while True:
        if left_block_id == right_block_id:
            if right_block_len > 0:
                res.extend(repeat(right_block_id, right_block_len))
            return res

        if add_left:
            # left blocks are not moved
            res.extend(repeat(left_block_id, dm.blocks[left_block_id]))
            left_block_id += 1
            add_left = False

        # move right block in the currently available free space
        if right_block_len < remaining:
            res.extend(repeat(right_block_id, right_block_len))
            remaining -= right_block_len
            right_block_id -= 1
            right_block_len = dm.blocks[right_block_id]
        elif right_block_len == remaining:
            res.extend(repeat(right_block_id, right_block_len))
            add_left = True
            free_id += 1
            remaining = dm.free[free_id]
            right_block_id -= 1
            right_block_len = dm.blocks[right_block_id]
        else:
            res.extend(repeat(right_block_id, remaining))
            right_block_len -= remaining
            add_left = True
            free_id += 1
            remaining = dm.free[free_id]


def checksum(blocks: list[int]) -> int:
    return sum([pos * block_id for pos, block_id in enumerate(blocks)])


def p1(input: DiskMap) -> int:
    return checksum(defrag(input))


# def p2(input: Map) -> int:
#     return len(input.all_antinodes(part2=True))


if __name__ == "__main__":
    input = read_input("d09", parser=parse)

    p1_ans = p1(input)
    assert p1_ans == 6471961544878
    print(f"p1: {p1_ans}")

#     p2_ans = p2(input)
#     assert p2_ans == 1184
#     print(f"p2: {p2_ans}")


def test_p1():
    input = read_test_input("d09", parser=parse)
    assert p1(input) == 1928


# def test_p2():
#     input = read_test_input("d08", parser=parse)
#     assert p2(input) == 34
