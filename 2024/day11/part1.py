#! /usr/bin/env python

from common import util

from functools import partial
import re

def process_line(stones, line):
    stones.extend([int(x) for x in line.strip().split()])

def blink(stones, num):
    for i in range(num):
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            else:
                num_digits = len(str(stone))
                if num_digits % 2 == 0:
                    new_stones.append(int(str(stone)[0:num_digits // 2]))
                    new_stones.append(int(str(stone)[num_digits // 2:]))
                else:
                    new_stones.append(stone * 2024)
        stones = new_stones
        print(f'after {i + 1} blinks: {new_stones}')
    return stones

def main():
    stones = []
    # util.read('day11/sample.txt', partial(process_line, stones))
    util.read('day11/input.txt', partial(process_line, stones))

    stones = blink(stones, 25)

    print(f'num stones = {len(stones)}')

if __name__ == '__main__':
    main()
