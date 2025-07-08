#! /usr/bin/env python

from common import util

from functools import partial
import re

def process_memory(instructions, memory):

    matches = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', memory)
    for match in matches:
        # print(match)
        assert len(match) == 2
        instructions.append((int(match[0]), int(match[1])))


def main():
    instructions = []
    util.read('day3/input.txt', partial(process_memory, instructions))

    print(f'result = {sum([a * b for (a, b) in instructions])}')

if __name__ == '__main__':
    main()
