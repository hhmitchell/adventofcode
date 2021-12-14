#! /usr/bin/env python

import math
import sys

OPEN_TO_CLOSE = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}
CLOSE_TO_OPEN = {}
for key in OPEN_TO_CLOSE:
    CLOSE_TO_OPEN[OPEN_TO_CLOSE[key]] = key

SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}


def get_corrupted_line_score(line):

    stack = []
    for char in line:
        if char in OPEN_TO_CLOSE:
            stack.append(char)
        elif char in CLOSE_TO_OPEN:
            if len(stack) == 0:
                return SCORE[char]
            opener = stack.pop()
            if CLOSE_TO_OPEN[char] != opener:
                return SCORE[char]

    return None


def main(args):
    lines = []
    with open(args[0], 'r') as f:
        for line in f.readlines():
            lines.append(list(line.strip()))

    scores = []
    for line in lines:
        score = get_corrupted_line_score(line)
        if score is not None:
            scores.append(score)

    print(sum(scores))


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
