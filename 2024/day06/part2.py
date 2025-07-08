#! /usr/bin/env python

from common import util

from functools import partial
import re

class LabMap():
    def __init__(self):
        self._rows = []
        self._init_guard = None

    def get_dir_indicator(self):
        if self._guard[2] == 0:
            if self._guard[3] == 1:
                return '>'
            return '<'
        if self._guard[2] == 1:
            return 'v'
        return '^'

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
        for guard in '<^>v':
            index = row.find(guard)
            if index != -1:
                direction = self.get_direction(guard)
                self._init_guard = [len(self._rows) - 1, index, direction[0], direction[1]]

    def go(self):
        self._visited = []
        for i in range(len(self._rows)):
            self._visited.append([])
            for j in range(len(self._rows[i])):
                self._visited[i].append(set())
        self._guard = self._init_guard.copy()
        # print(f'guard = {self._guard}')
        row = self._guard[0]
        col = self._guard[1]
        while row >= 0 and row < len(self._rows) and col >= 0 and col < len(self._rows[row]):
            dir_indicator = self.get_dir_indicator()
            # print(f'trying {row}, {col} {dir_indicator}')
            if dir_indicator in self._visited[row][col]:
                # print(f'already visited [{row}][{col}] in direction {self._rows[row][col]}')
                return False
            self._visited[row][col].add(dir_indicator)
            next_row = row + self._guard[2]
            next_col = col + self._guard[3]
            if next_row >= 0 and next_row < len(self._rows) and next_col >= 0 and next_col < len(self._rows[row]) and self._rows[next_row][next_col] == '#':
                self.rotate_guard()
            else:
                row = next_row
                col = next_col

        return True

    def get_possible_obstructions(self):
        obstructions = []
        for i, j in self.get_candidates():
            orig = self._rows[i][j]
            self._rows[i][j] = '#'
            # print(f'trying candidate {i},{j}')
            if not self.go():
                obstructions.append((i, j))
            self._rows[i][j] = orig

        # print(obstructions)
        return len(obstructions)


    def get_candidates(self):
        candidates = []
        for i in range(len(self._visited)):
            for j in range(len(self._visited[i])):
                if self._visited[i][j]:
                    candidates.append((i, j))

        return candidates

    def get_total(self):
        total = 0
        for row in self._visited:
            total += sum([1 if len(x) else 0 for x in row])

        return total

def read_map(lab_map, line):
    lab_map.add_row(line.strip())

def main():
    lab_map = LabMap()
    # util.read('day6/sample.txt', partial(read_map, lab_map))
    util.read('day6/input.txt', partial(read_map, lab_map))

    assert(lab_map.go())
    total = lab_map.get_possible_obstructions()
    print(f'possible obstructions = {total}')

if __name__ == '__main__':
    main()
