#! /usr/bin/env python

import re
import sys

ORIENTATIONS = [
    (1, 2, 3),  # good
    (1, -2, -3),
    (1, 3, -2),
    (1, -3, 2),
    (-1, 3, 2),
    (-1, -3, -2),
    (-1, -2, 3),
    (-1, 2, -3),  # good
    (2, 3, 1),
    (2, -3, -1),  # good
    (2, -1, 3),
    (2, 1, -3),  # good
    (-2, 1, 3),
    (-2, -1, -3),
    (-2, -3, 1),
    (-2, 3, -1),
    (3, 1, 2),
    (3, -1, -2),
    (3, -2, 1),
    (3, 2, -1),
    (-3, 2, 1),
    (-3, -2, -1),
    (-3, -1, 2),
    (-3, 1, -2),
]


class Scanner:
    def __init__(self, id):
        self.id = id
        self.beacons = set()

    def __str__(self):
        lines = []
        lines.append('Scanner {}'.format(self.id))
        for beacon in self.beacons:
            lines.append('  {}'.format(beacon))
        return '\n'.join(lines)

    def add_beacon(self, beacon):
        self.beacons.add(beacon)

    def find_common_beacons(self, other):
        for orientation in ORIENTATIONS:
            for self_beacon in self.beacons:
                for other_beacon in other.beacons:
                    transform = get_transform(
                        self_beacon, orient_beacon(other_beacon, orientation))
                    mapped = []
                    for target in other.beacons:
                        base = apply_transform(
                            orient_beacon(target, orientation), transform,
                            True)
                        if base in self.beacons:
                            mapped.append((base, target))
                    if len(mapped) >= 12:
                        return (orientation, transform, mapped)

        return None


def orient_beacon(beacon, orientation):
    xi = abs(orientation[0]) - 1
    yi = abs(orientation[1]) - 1
    zi = abs(orientation[2]) - 1
    xm = 1 if orientation[0] > 0 else -1
    ym = 1 if orientation[1] > 0 else -1
    zm = 1 if orientation[2] > 0 else -1
    return (beacon[xi] * xm, beacon[yi] * ym, beacon[zi] * zm)


def get_transform(base, target):
    return (target[0] - base[0], target[1] - base[1], target[2] - base[2])


def apply_transform(base, transform, reverse=False):
    if reverse:
        return (base[0] - transform[0], base[1] - transform[1],
                base[2] - transform[2])
    return (base[0] + transform[0], base[1] + transform[1],
            base[2] + transform[2])


def get_path(graph, start, end):
    visited = set()
    stack = [[start]]
    path = []
    while stack:
        if stack[-1]:
            current = stack[-1].pop()
        else:
            stack.pop()
            if path:
                path.pop()
            continue

        path.append(current)
        visited.add(current)
        neighbors = graph[current]
        if end in neighbors:
            path.append(end)
            return path

        have_neighbor = False
        visitable_neighbors = [n for n in neighbors if n not in visited]
        if len(visitable_neighbors) > 0:
            stack.append(visitable_neighbors)
            have_neighbor = True
        if not have_neighbor:
            path.pop()


def main(args):
    scanners = []
    scanner = None
    with open(args[0], 'r') as f:
        line = f.readline()
        while line:
            line = line.strip()
            if scanner is None:
                match = re.fullmatch('--- scanner (.+) ---', line)
                scanner = Scanner(int(match.group(1)))
            elif line:
                coordinates = tuple([int(n) for n in line.split(',')])
                scanner.add_beacon(coordinates)
            else:
                scanners.append(scanner)
                scanner = None
            line = f.readline()
        if scanner is not None:
            scanners.append(scanner)
            scanner = None

    scanner_ids = set(range(1, len(scanners)))
    results = {}
    results[0] = (None, ORIENTATIONS[0], (0, 0, 0))
    result_ids = [[0]]
    while scanner_ids:
        new_result_ids = []
        for base_id in result_ids[-1]:
            target_ids = list(scanner_ids)
            for target_id in target_ids:
                if target_id not in result_ids[-1]:
                    print('attempt to find common beacons between {} and {}'.
                          format(base_id, target_id))
                    common_beacons = scanners[base_id].find_common_beacons(
                        scanners[target_id])
                    if common_beacons:
                        print('push {}, {}'.format(target_id, base_id))
                        results[target_id] = (base_id, common_beacons[0],
                                              common_beacons[1],
                                              common_beacons[2])
                        new_result_ids.append(target_id)
                        scanner_ids.remove(target_id)
            if new_result_ids:
                print('append new result_ids')
                result_ids.append(new_result_ids)
    for result in result_ids:
        print('R = {}'.format(result))

    for i in results:
        print('result[{}] = {}'.format(i, results[i]))

    all_beacons = set([(beacon, 0, beacon) for beacon in scanners[0].beacons])
    for i in range(1, len(scanners)):
        target_id = i
        print('attempt target_id {}'.format(i))
        for beacon in scanners[i].beacons:
            pos = beacon
            while True:
                result = results[target_id]
                base_id = result[0]
                orientation = result[1]
                transform = result[2]

                pos = orient_beacon(pos, orientation)
                pos = apply_transform(pos, transform, True)
                if base_id == 0:
                    all_beacons.add((pos, i, beacon))
                    break
                target_id = base_id
        print('common beacons between {} and {}'.format(i, results[i][0]))
        for pair in results[i][3]:
            pos = pair[1]
            print('orig: {}, '.format(pos), end='')
            while True:
                result = results[target_id]
                base_id = result[0]
                orientation = result[1]
                transform = result[2]

                pos = orient_beacon(pos, orientation)
                pos = apply_transform(pos, transform, True)
                if base_id == 0:
                    print('at 0: {}'.format(pos))
                    break
                target_id = base_id
    print(len(all_beacons))
    for b in sorted(all_beacons):
        print(b)

    #graph = {}
    #for pair in results:
    #    print('results[{}] = {}'.format(pair, results[pair]))
    #    if pair[0] not in graph:
    #        graph[pair[0]] = set()
    #    if pair[1] not in graph:
    #        graph[pair[1]] = set()
    #    graph[pair[0]].add(pair[1])
    #    graph[pair[1]].add(pair[0])

    #print(graph)
    #all_beacons = set(scanners[0].beacons)
    #for i in range(1, len(scanners)):
    #    path = get_path(graph, i, 0)
    #    print('path from {} to 0: {}'.format(i, path))
    #    for beacon in scanners[i].beacons:
    #        pos = beacon
    #        for j in range(len(path) - 1):
    #            start = path[j]
    #            next = path[j + 1]
    #            if start > next:
    #                (orientation, transform) = (results[(next, start)][0],
    #                                            results[(next, start)][1])
    #                pos = orient_beacon(pos, orientation)
    #                pos = apply_transform(pos, transform, True)
    #            else:
    #                (orientation, transform) = (results[(start, next)][0],
    #                                            results[(start, next)][1])
    #                pos = apply_transform(pos, transform)
    #                pos = orient_beacon(pos, orientation)
    #        all_beacons.add(pos)
    #print(len(all_beacons))
    #for beacon in sorted(all_beacons):
    #    print(beacon)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
