from aoc.helpers import *
from dataclasses import dataclass, field
from itertools import repeat
from copy import deepcopy
from collections import defaultdict


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
            # if we have more free space than the block's length, move it fully,
            # update the remaining space, and move on to the next block from the right
            res.extend(repeat(right_block_id, right_block_len))

            remaining -= right_block_len
            right_block_id -= 1
            right_block_len = dm.blocks[right_block_id]
        elif right_block_len == remaining:
            # if we can fit the remaining right block part fully into the free space with no free space left,
            # do that and advance to the next free space and the next block from the right;
            # also don't forget to fill-in the block from the left that is after the used free space
            res.extend(repeat(right_block_id, right_block_len))

            add_left = True
            free_id += 1
            remaining = dm.free[free_id]

            right_block_id -= 1
            right_block_len = dm.blocks[right_block_id]
        else:
            # if the block won't fit in the remaining space, put everything we can in the space,
            # update the remaining right block length, and advance to the next free space,
            # while also not forgetting about left block fill-in
            res.extend(repeat(right_block_id, remaining))

            right_block_len -= remaining

            add_left = True
            free_id += 1
            remaining = dm.free[free_id]


def checksum(blocks: list[int]) -> int:
    return sum([pos * block_id for pos, block_id in enumerate(blocks)])


def p1(input: DiskMap) -> int:
    return checksum(defrag(input))


def defrag_whole_files(dm: DiskMap):
    # maintaining a copy of free spaces that we update as we go,
    # move whole files to the leftmost free blocks that can contain them,
    # recording the moves in the `moves` dict
    moves, free = {}, deepcopy(dm.free)
    for block_id in reversed(range(len(dm.blocks))):
        for free_id in range(min(len(free) - 1, block_id)):
            if free[free_id] >= dm.blocks[block_id]:
                moves[block_id] = free_id
                free[free_id] -= dm.blocks[block_id]
                free[block_id - 1] += dm.blocks[block_id]
                print(f"moving {block_id} to {free_id}, free: {free}")
                break

    # convert block_id -> free_id moves mapping to free_id -> [block_id, block_id, ...]
    # where block ids are sorted in decreasing order
    free_to_moved = defaultdict(list)
    for block_id, free_id in moves.items():
        free_to_moved[free_id].append(block_id)
    for free_id in free_to_moved.keys():
        free_to_moved[free_id].sort(reverse=True)
    print(f"moves = {moves}")
    print(f"free = {free}")
    print(f"free_to_moved = {free_to_moved}")

    res, free_id = [], 0
    for block_id in range(len(dm.blocks)):
        if block_id in moves:
            res.extend(repeat(0, free[free_id]))
            free_id += 1
        else:
            res.extend(repeat(block_id, dm.blocks[block_id]))

        # free_id = block_id
        if free_id in free_to_moved:
            remaining_free = dm.free[free_id]
            for block_id in free_to_moved[free_id]:
                block_len = dm.blocks[block_id]
                res.extend(repeat(block_id, block_len))
                remaining_free -= block_len
            if remaining_free > 0:
                res.extend(repeat(0, remaining_free))
        elif free_id >= len(dm.free):
            # add all remaining space to the end - we need to also keep in mind that block with id 0 is not
            # distinguishable in the output from the free space also marked with 0, that's why we need to
            # add the 0 block length here
            res.extend(repeat(0, sum(dm.free) + dm.blocks[0] - res.count(0)))
        else:
            res.extend(repeat(0, dm.free[free_id]))
        print(f"res = {res}")
    return res


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
