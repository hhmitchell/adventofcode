#! /usr/bin/env python

from common import util

from functools import partial
import re

def process_line(line):
    id = 0
    block = []
    for i in range(len(line.strip())):
        if i % 2 == 0:
            block.extend([str(id)] * int(line[i]))
            id += 1
        else:
            block.extend(['.'] * int(line[i]))

    left_free = block.index('.', 0)
    right = len(block) - 1
    while left_free < right:
        if block[right] != '.':
            block[left_free] = block[right]
            block[right] = '.'
            left_free = block.index('.', left_free + 1)
        right -= 1

    checksum = 0
    for i in range(len(block)):
        if block[i] != '.':
            checksum += (i * int(block[i]))
    print(f'checksum = {checksum}')


def main():
    # util.read('day09/sample.txt', partial(process_line))
    util.read('day09/input.txt', partial(process_line))

if __name__ == '__main__':
    main()
