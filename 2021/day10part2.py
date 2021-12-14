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
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def get_incomplete_line(line):
    stack = []
    for char in line:
        if char in OPEN_TO_CLOSE:
            stack.append(char)
        elif char in CLOSE_TO_OPEN:
            if len(stack) == 0:
                return None
            opener = stack.pop()
            if CLOSE_TO_OPEN[char] != opener:
                return None

    return stack


def get_autocomplete(stack):
    stack.reverse()
    autocomplete = []
    for char in stack:
        autocomplete.append(OPEN_TO_CLOSE[char])

    return autocomplete


def get_score(autocomplete):
    score = 0
    for char in autocomplete:
        score *= 5
        score += SCORE[char]

    return score


def main(args):
    lines = []
    with open(args[0], 'r') as f:
        for line in f.readlines():
            lines.append(list(line.strip()))

    scores = []
    for line in lines:
        stack = get_incomplete_line(line)
        if stack is not None and len(stack) > 0:
            autocomplete = get_autocomplete(stack)
            scores.append(get_score(autocomplete))

    scores.sort()
    print(scores[int(len(scores) / 2)])


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
