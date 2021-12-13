#! /usr/bin/env python

import sys


def main(args):
    fishes = [0] * 9
    with open(args[0], 'r') as f:
        for line in f.readlines():
            for n in line.strip().split(','):
                fishes[int(n)] += 1

    print(fishes)
    print(sum(fishes))

    num_days = 256
    for i in range(num_days):
        new_fishes = 0
        for j in range(len(fishes)):
            if j == 0:
                new_fishes = fishes[j]
            else:
                fishes[j - 1] = fishes[j]
        fishes[6] += new_fishes
        fishes[8] = new_fishes

    print(sum(fishes))


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
