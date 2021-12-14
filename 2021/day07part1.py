#! /usr/bin/env python

import sys


def main(args):
    crabs = [0] * 9
    with open(args[0], 'r') as f:
        for line in f.readlines():
            for n in line.strip().split(','):
                num = int(n)
                if len(crabs) < num + 1:
                    crabs.extend([0] * (num + 1 - len(crabs)))
                crabs[num] += 1

    fuel = [0] * len(crabs)
    for i in range(len(crabs)):
        for j in range(len(crabs)):
            fuel[i] += crabs[j] * abs(i - j)

    print(fuel.index(min(fuel)))
    print(min(fuel))


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
