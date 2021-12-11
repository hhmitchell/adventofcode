#! /usr/bin/env python

import sys


def main(args):
    measurements = []
    with open(args[0], 'r') as f:
        lines = f.readlines()
        measurements = [int(line.strip()) for line in lines]

    window_size = 3
    window = None
    previous_window = None
    num_larger = 0
    for index in range(len(measurements) - 2):
        window = sum(measurements[index:index + window_size])
        if previous_window is not None and window > previous_window:
            num_larger += 1
        previous_window = window

    print(num_larger)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
