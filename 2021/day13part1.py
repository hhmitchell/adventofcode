#! /usr/bin/env python

import re
import sys


def extend_paper(paper, point):
    if point[1] + 1 > len(paper):
        foo = [False for i in range(len(paper[0]))]
        bar = [foo.copy() for i in range(point[1] - len(paper) + 1)]
        paper.extend(bar)

    if point[0] + 1 > len(paper[0]):
        foo2 = [False for i in range(point[0] - len(paper[0]) + 1)]
        for vent_line in paper:
            vent_line.extend(foo2)


def fold(paper, instruction):
    new_paper = []
    if instruction[0] == 'x':
        if instruction[1] > len(paper[0]):
            print('ERROR? {}x{} with instruction {}'.format(
                len(paper), len(paper[0]), instruction))
            return []
        row = [False] * instruction[1]
        for i in range(len(paper)):
            new_paper.append(row.copy())

        for i in range(len(new_paper)):
            for j in range(len(new_paper[i])):
                new_paper[i][j] = paper[i][j] or paper[i][len(paper[i]) - j -
                                                          1]

    elif instruction[0] == 'y':
        if instruction[1] > len(paper):
            print('ERROR? {}x{} with instruction {}'.format(
                len(paper), len(paper[0]), instruction))
            return []
        row = [False] * len(paper[0])
        for i in range(instruction[1]):
            new_paper.append(row.copy())

        for i in range(len(new_paper)):
            for j in range(len(new_paper[i])):
                new_paper[i][j] = paper[i][j] or paper[len(paper) - i - 1][j]

    return new_paper


def main(args):
    paper = [[]]
    instructions = []
    with open(args[0], 'r') as f:
        lines = f.readlines()
        i = 0
        for i in range(len(lines)):
            line = lines[i].strip()
            if len(line) == 0:
                break
            point = [int(x) for x in line.split(',')]
            extend_paper(paper, point)
            paper[point[1]][point[0]] = True
        for line in lines[i + 1:]:
            match = re.fullmatch('fold along (.)=(.+)', line.strip())
            instructions.append((match.group(1), int(match.group(2))))

    for instruction in instructions[:1]:
        paper = fold(paper, instruction)

    num_visible = 0
    for row in paper:
        for point in row:
            if point:
                num_visible += 1
    print(num_visible)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
