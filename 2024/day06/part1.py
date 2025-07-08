#! /usr/bin/env python

from common import util

from functools import partial
import re

class LabMap():
    def __init__(self):
        self._rows = []
        self._guard = None
        self._visited = []

    def get_direction(self, guard):
        if guard == '<':
            return (0, -1)
        if guard == '^':
            return (-1, 0)
        if guard == '>':
            return (0, 1)
        # if guard == 'v':
        return (1, 0)

    def rotate_guard(self):
        if self._guard[2] == 0:
            if self._guard[3] == 1:
                self._guard[2] = 1
                self._guard[3] = 0
                return
            else:
                self._guard[2] = -1
                self._guard[3] = 0
                return
        if self._guard[2] == 1:
            self._guard[2] = 0
            self._guard[3] = -1
            return
        self._guard[2] = 0
        self._guard[3] = 1

    def add_row(self, row):
        self._rows.append([char for char in row])
        self._visited.append([char for char in row])
        for guard in '<^>v':
            index = row.find(guard)
            if index != -1:
                direction = self.get_direction(guard)
                self._guard = [len(self._rows) - 1, index, direction[0], direction[1]]

    def go(self):
        row = self._guard[0]
        col = self._guard[1]
        print(f'starting at {row}, {col}')
        while row >= 0 and row < len(self._rows) and col >= 0 and col < len(self._rows[row]):
            self._visited[row][col] = 'X'
            next_row = row + self._guard[2]
            next_col = col + self._guard[3]
            if next_row >= 0 and next_row < len(self._rows) and next_col >= 0 and next_col < len(self._rows[row]) and self._rows[next_row][next_col] == '#':
                self.rotate_guard()
            else:
                row = next_row
                col = next_col

    def get_total(self):
        total = 0
        for row in self._visited:
            total += sum([1 if x == 'X' else 0 for x in row])

        return total

    def __iter__(self):
        for row in self._visited:
            yield row

def read_map(lab_map, line):
    lab_map.add_row(line.strip())

def main():
    lab_map = LabMap()
    util.read('day6/input.txt', partial(read_map, lab_map))

    lab_map.go()
    total = lab_map.get_total()
    print(f'distinct positions = {total}')

if __name__ == '__main__':
    main()
