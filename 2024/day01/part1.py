#! /usr/bin/env python

from common import util

from functools import partial
import re

def process_line(left, right, line):
    parts = re.split(r' +', line)
    left.append(int(parts[0]))
    right.append(int(parts[1]))

def main():
    left = []
    right = []
    util.read('day1/input.txt', partial(process_line, left, right))
    left.sort()
    right.sort()

    total = 0
    for i in range(len(left)):
        total += abs(left[i] - right[i])

    print(f'total distance = {total}')

if __name__ == '__main__':
    main()
