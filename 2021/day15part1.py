#! /usr/bin/env python

import sys


def get_neighbors(cavern, i, j, visited):
    neighbors = []
    if i > 0 and (i - 1, j) not in visited:
        neighbors.append((i - 1, j))
    if j > 0 and (i, j - 1) not in visited:
        neighbors.append((i, j - 1))
    if j < len(cavern[i]) - 1 and (i, j + 1) not in visited:
        neighbors.append((i, j + 1))
    if i < len(cavern) - 1 and (i + 1, j) not in visited:
        neighbors.append((i + 1, j))
    return neighbors


def get_current(tentative_risk, visited):
    current = None
    for i in range(len(tentative_risk)):
        for j in range(len(tentative_risk[i])):
            if (i, j) in visited:
                continue
            risk = tentative_risk[i][j]
            if risk is not None and (current is None or risk < current[1]):
                current = ((i, j), risk)

    return current[0]


def calculate_risk(cavern, start, end):
    visited = set()
    row = [None for i in range(len(cavern[0]))]
    tentative_risk = [row.copy() for i in range(len(cavern))]
    tentative_risk[start[0]][start[1]] = 0
    while end not in visited:
        current = get_current(tentative_risk, visited)
        current_risk = tentative_risk[current[0]][current[1]]
        neighbors = get_neighbors(cavern, current[0], current[1], visited)
        for neighbor in neighbors:
            i = neighbor[0]
            j = neighbor[1]
            risk = cavern[i][j] + current_risk
            if tentative_risk[i][j] is None or risk < tentative_risk[i][j]:
                tentative_risk[i][j] = cavern[i][j] + current_risk
        visited.add(current)

    return tentative_risk[end[0]][end[1]]


def main(args):
    cavern = []
    with open(args[0], 'r') as f:
        lines = f.readlines()
        for line in lines:
            cavern.append([int(x) for x in list(line.strip())])

    print(calculate_risk(cavern, (0, 0),
                         (len(cavern) - 1, len(cavern[0]) - 1)))


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
