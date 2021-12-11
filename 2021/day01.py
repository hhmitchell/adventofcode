#! /usr/bin/env python

import sys


def main(args):
    previous_measurement = None
    num_larger = 0
    with open(args[0], 'r') as f:
        lines = f.readlines()
        for line in lines:
            measurement = int(line.strip())
            if previous_measurement is not None and measurement > previous_measurement:
                num_larger += 1
            previous_measurement = measurement

    print(num_larger)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
