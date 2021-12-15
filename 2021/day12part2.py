#! /usr/bin/env python

import math
import sys


def find_paths(caves, start, end):
    paths = []
    stack = [[start]]
    current_path = []

    while stack:
        if stack[-1]:
            cave = stack[-1].pop()
        else:
            stack.pop()
            if current_path:
                current_path.pop()
            continue

        current_path.append(cave)

        if cave == end:
            paths.append(current_path.copy())
            current_path.pop()
            continue

        unvisitable_neighbors = set([start])
        small_caves_in_current_path = [
            cave for cave in current_path if cave.islower() and cave != start
        ]
        unique_small_caves = set(small_caves_in_current_path)
        if len(small_caves_in_current_path) != len(unique_small_caves):
            unvisitable_neighbors = unvisitable_neighbors.union(
                unique_small_caves)
        visitable_neighbors = list(caves[cave] - unvisitable_neighbors)

        if len(visitable_neighbors) == 0:
            current_path.pop()
        else:
            stack.append(sorted(visitable_neighbors))

    return paths


def main(args):
    caves = {}
    with open(args[0], 'r') as f:
        for line in f.readlines():
            pair = line.strip().split('-')
            if pair[0] not in caves:
                caves[pair[0]] = set()
            caves[pair[0]].add(pair[1])
            if pair[1] not in caves:
                caves[pair[1]] = set()
            caves[pair[1]].add(pair[0])

    paths = find_paths(caves, 'start', 'end')
    print(len(paths))


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
