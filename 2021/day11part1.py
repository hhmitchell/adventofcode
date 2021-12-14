#! /usr/bin/env python

import math
import sys


def maybe_flash(octopi, i, j, flashed):
    if flashed[i][j] == 0:
        octopi[i][j] += 1
        if octopi[i][j] > 9:
            flashed[i][j] = 1
            octopi[i][j] = 0
            if i > 0:
                if j > 0:
                    maybe_flash(octopi, i - 1, j - 1, flashed)
                maybe_flash(octopi, i - 1, j, flashed)
                if j < len(octopi[i]) - 1:
                    maybe_flash(octopi, i - 1, j + 1, flashed)
            if j > 0:
                maybe_flash(octopi, i, j - 1, flashed)
            if j < len(octopi[i]) - 1:
                maybe_flash(octopi, i, j + 1, flashed)
            if i < len(octopi) - 1:
                if j > 0:
                    maybe_flash(octopi, i + 1, j - 1, flashed)
                maybe_flash(octopi, i + 1, j, flashed)
                if j < len(octopi[i]) - 1:
                    maybe_flash(octopi, i + 1, j + 1, flashed)


def step(octopi):
    flashed = []
    for i in range(len(octopi)):
        flashed.append([0] * len(octopi))

    for i in range(len(octopi)):
        for j in range(len(octopi[i])):
            maybe_flash(octopi, i, j, flashed)

    return sum([sum(row) for row in flashed])


def main(args):
    octopi = []
    with open(args[0], 'r') as f:
        for line in f.readlines():
            octopi.append([int(n) for n in list(line.strip())])

    num_steps = 100
    num_flashes = 0
    for i in range(num_steps):
        num_flashes += step(octopi)

    print(num_flashes)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
