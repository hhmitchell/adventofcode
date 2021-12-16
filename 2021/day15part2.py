#! /usr/bin/env python

import sys


def get_cavern(tile):
    repeat = 5
    row = [None for i in range(repeat * len(tile[0]))]
    cavern = [row.copy() for i in range(repeat * len(tile))]
    for i in range(len(tile)):
        cavern[i][0:len(tile[i])] = tile[i]
    for i in range(1, repeat):
        for x in range(len(tile)):
            parent_row = cavern[x + (i - 1) * len(tile)][0:len(tile[x])]
            cavern[x + (i * len(tile))][0:len(tile[x])] = [
                value + 1 if value < 9 else 1 for value in parent_row
            ]
    for i in range(1, repeat):
        for x in range(len(cavern)):
            parent_row = cavern[x][(i - 1) * len(tile):i * len(tile)]
            cavern[x][i * len(tile):(i + 1) * len(tile)] = [
                value + 1 if value < 9 else 1 for value in parent_row
            ]
    return cavern


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


def get_current(tentative_risk, calculated, visited):
    current = None
    for node in calculated - visited:
        risk = tentative_risk[node[0]][node[1]]
        if current is None or risk < current[1]:
            current = ((node[0], node[1]), risk)

    return current[0]


def calculate_risk(cavern, start, end):
    visited = set()
    calculated = set()
    calculated.add(start)
    row = [None for i in range(len(cavern[0]))]
    tentative_risk = [row.copy() for i in range(len(cavern))]
    tentative_risk[start[0]][start[1]] = 0
    while end not in visited:
        current = get_current(tentative_risk, calculated, visited)
        current_risk = tentative_risk[current[0]][current[1]]
        neighbors = get_neighbors(cavern, current[0], current[1], visited)
        for neighbor in neighbors:
            i = neighbor[0]
            j = neighbor[1]
            risk = cavern[i][j] + current_risk
            if tentative_risk[i][j] is None or risk < tentative_risk[i][j]:
                tentative_risk[i][j] = cavern[i][j] + current_risk
            calculated.add(neighbor)
        visited.add(current)
        calculated.remove(current)

    return tentative_risk[end[0]][end[1]]


def main(args):
    tile = []
    with open(args[0], 'r') as f:
        lines = f.readlines()
        for line in lines:
            tile.append([int(x) for x in list(line.strip())])
    cavern = get_cavern(tile)

    print(calculate_risk(cavern, (0, 0),
                         (len(cavern) - 1, len(cavern[0]) - 1)))


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
