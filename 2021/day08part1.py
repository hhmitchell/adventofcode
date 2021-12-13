#! /usr/bin/env python

import sys


def main(args):
    signals = []
    with open(args[0], 'r') as f:
        for line in f.readlines():
            parts = line.strip().split(' | ')
            patterns = parts[0].split()
            values = parts[1].split()
            signals.append((patterns, values))

    num_unique_patterns = 0
    for signal in signals:
        values = signal[1]
        for value in values:
            length = len(value)
            if length == 2 or length == 3 or length == 4 or length == 7:
                num_unique_patterns += 1
    print(num_unique_patterns)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
