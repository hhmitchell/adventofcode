#! /usr/bin/env python

import sys


def get_low_points(heightmap):
    low_points = []
    for i in range(len(heightmap)):
        for j in range(len(heightmap[i])):
            is_low = True
            if i > 0:
                if heightmap[i][j] >= heightmap[i - 1][j]:
                    is_low = False
            if not is_low:
                continue
            if j > 0:
                if heightmap[i][j] >= heightmap[i][j - 1]:
                    is_low = False
            if not is_low:
                continue
            if i < len(heightmap) - 1:
                if heightmap[i][j] >= heightmap[i + 1][j]:
                    is_low = False
            if not is_low:
                continue
            if j < len(heightmap[i]) - 1:
                if heightmap[i][j] >= heightmap[i][j + 1]:
                    is_low = False
            if not is_low:
                continue

            low_points.append((i, j, heightmap[i][j]))

    return low_points


def main(args):
    heightmap = []
    with open(args[0], 'r') as f:
        for line in f.readlines():
            heightmap.append([int(height) for height in list(line.strip())])

    low_points = get_low_points(heightmap)
    print(sum([height + 1 for (i, j, height) in low_points]))


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
