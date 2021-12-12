#! /usr/bin/env python

import sys


def main(args):
    horizontal_pos = 0
    depth = 0
    aim = 0
    with open(args[0], 'r') as f:
        lines = f.readlines()
        for line in lines:
            command = line.strip().split(' ')
            direction = command[0]
            units = int(command[1])
            if direction == 'forward':
                horizontal_pos += units
                depth += aim * units
            elif direction == 'down':
                aim += units
            elif direction == 'up':
                aim -= units

    print(horizontal_pos * depth)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
