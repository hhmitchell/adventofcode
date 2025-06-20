#! /usr/bin/env python

from common import util

from functools import partial
import re

def process_line(left, right, line):
    parts = re.split(r' +', line)
    l = int(parts[0])
    r = int(parts[1])
    if l in left:
        left[l] += 1
    else:
        left[l] = 1
    if r in right:
        right[r] += 1
    else:
        right[r] = 1

def main():
    left = {}
    right = {}
    util.read('day1/input.txt', partial(process_line, left, right))

    total = 0
    for k in left.keys():
        if k in right:
            total += k * left[k] * right[k]

    print(f'total similarity = {total}')

if __name__ == '__main__':
    main()
