#! /usr/bin/env python

import math
import sys


def get_neighbors(heightmap, point):
    neighbors = set()
    i = point[0]
    j = point[1]
    if i > 0:
        if heightmap[i - 1][j] < 9:
            neighbors.add((i - 1, j))
    if j > 0:
        if heightmap[i][j - 1] < 9:
            neighbors.add((i, j - 1))
    if i < len(heightmap) - 1:
        if heightmap[i + 1][j] < 9:
            neighbors.add((i + 1, j))
    if j < len(heightmap[i]) - 1:
        if heightmap[i][j + 1] < 9:
            neighbors.add((i, j + 1))

    return neighbors


def get_basin(heightmap, start):
    visited = set()
    stack = [start]
    while stack:
        point = stack.pop()
        if point not in visited:
            visited.add(point)
            neighbors = get_neighbors(heightmap, point)
            stack.extend(list(neighbors - visited))

    return visited


def main(args):
    heightmap = []
    with open(args[0], 'r') as f:
        for line in f.readlines():
            heightmap.append([int(height) for height in list(line.strip())])

    visited = set()
    basins = []
    for i in range(len(heightmap)):
        for j in range(len(heightmap[i])):
            if heightmap[i][j] < 9 and (i, j) not in visited:
                basin = get_basin(heightmap, (i, j))
                visited.update(basin)
                basins.append(basin)

    sizes = sorted([len(basin) for basin in basins])[-3:]
    print(math.prod(sizes))


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
