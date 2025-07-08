#! /usr/bin/env python

from common import util

from functools import partial
import re

def get_mul(match):
    return (int(match.groups()[0]), int(match.groups()[1]))

def process_memory(instructions, state, memory):
    mul_matches = re.finditer(r'mul\((\d{1,3}),(\d{1,3})\)', memory)
    do_matches = re.finditer(r'do(n\'t)?\(\)', memory)

    mul_match = next(mul_matches, None)
    do_match = next(do_matches, None)
    while mul_match is not None:
        if do_match:
            if mul_match.start() < do_match.start():
                if state.enabled:
                    instructions.append(get_mul(mul_match))
                mul_match = next(mul_matches, None)
            else:
                state.enabled = do_match.groups()[0] is None
                do_match = next(do_matches, None)
            continue

        if state.enabled:
            instructions.append(get_mul(mul_match))
            mul_match = next(mul_matches, None)
        else:
            break


class State():
    def __init__(self):
        self.enabled = True

def main():
    instructions = []
    state = State()
    util.read('day3/input.txt', partial(process_memory, instructions, state))

    print(f'result = {sum([a * b for (a, b) in instructions])}')

if __name__ == '__main__':
    main()
