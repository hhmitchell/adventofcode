#! /usr/bin/env python

import sys


def read_vent(line):
    parts = line.split(' -> ')
    start = parts[0].split(',')
    end = parts[1].split(',')
    return ((int(start[0]), int(start[1])), (int(end[0]), int(end[1])))


def extend_vents(vent_lines, point):
    if point[0] + 1 > len(vent_lines):
        foo = [0 for i in range(len(vent_lines[0]))]
        bar = [foo.copy() for i in range(point[0] - len(vent_lines) + 1)]
        vent_lines.extend(bar)

    if point[1] + 1 > len(vent_lines[0]):
        foo2 = [0 for i in range(point[1] - len(vent_lines[0]) + 1)]
        for vent_line in vent_lines:
            vent_line.extend(foo2)


def update_vents(vent_lines, vent):
    if not (vent[0][0] == vent[1][0] or vent[0][1] == vent[1][1]):
        return

    x_step = 1 if vent[0][0] < vent[1][0] else -1
    for x in range(vent[0][0], vent[1][0] + x_step, x_step):
        y_step = 1 if vent[0][1] < vent[1][1] else -1
        for y in range(vent[0][1], vent[1][1] + y_step, y_step):
            vent_lines[x][y] += 1


def count_danger(vent_lines):
    num_points = 0
    for line in vent_lines:
        for point in line:
            if point > 1:
                num_points += 1

    return num_points


def main(args):
    vent_lines = [[]]
    with open(args[0], 'r') as f:
        for line in f.readlines():
            vent = read_vent(line.strip())
            extend_vents(vent_lines, vent[0])
            extend_vents(vent_lines, vent[1])
            update_vents(vent_lines, vent)

    print(count_danger(vent_lines))


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
