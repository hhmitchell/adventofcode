#! /usr/bin/env python

import sys


def main(args):
    fishes = []
    with open(args[0], 'r') as f:
        for line in f.readlines():
            fishes.extend(int(n) for n in line.strip().split(','))

    num_days = 80
    for i in range(num_days):
        new_fishes = []
        for j in range(len(fishes)):
            if fishes[j] == 0:
                fishes[j] = 6
                new_fishes.append(8)
            else:
                fishes[j] -= 1
        fishes.extend(new_fishes)
        if i == 17:
            print(len(fishes))

    print(len(fishes))


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
