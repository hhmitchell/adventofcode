#! /usr/bin/env python

from common import util

from functools import partial
import re

def process_line(stones, line):
    for x in line.strip().split():
        stones[int(x)] = stones.get(int(x), 0) + 1

def blink(stones, num):
    cache = {}
    for i in range(num):
        new_stones = {}
        for stone, count in stones.items():
            if stone not in cache:
                temp = []
                if stone == 0:
                    temp.append(1)
                else:
                    num_digits = len(str(stone))
                    if num_digits % 2 == 0:
                        temp.append(int(str(stone)[0:num_digits // 2]))
                        temp.append(int(str(stone)[num_digits // 2:]))
                    else:
                        temp.append(stone * 2024)
                cache[stone] = temp

            for new_stone in cache[stone]:
                new_stones[new_stone] = new_stones.get(new_stone, 0) + count

        stones = new_stones
    return stones

def main():
    stones = {}
    # util.read('day11/sample.txt', partial(process_line, stones))
    util.read('day11/input.txt', partial(process_line, stones))

    stones = blink(stones, 75)

    print(f'num stones = {sum(num for num in stones.values())}')

if __name__ == '__main__':
    main()
