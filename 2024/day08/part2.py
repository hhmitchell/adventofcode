#! /usr/bin/env python

from common import util

from functools import partial
import re

class AntennaMap():
    def __init__(self):
        self._antennae = {}
        self._height = 0
        self._width = 0

    def is_valid(self, antinode):
        return antinode[0] >= 0 and antinode[0] < self._height and antinode[1] >= 0 and antinode[1] < self._width

    def add_row(self, row):
        self._height += 1
        self._width = len(row)
        for match in re.finditer(r'[a-zA-Z0-9]', row):
            antenna = row[match.start()]
            if antenna not in self._antennae:
                self._antennae[antenna] = []
            self._antennae[antenna].append((self._height - 1, match.start()))

    def get_antinodes(self):
        antinodes = set()
        for antenna in self._antennae:
            for i in range(len(self._antennae[antenna]) - 1):
                for j in range(i + 1, len(self._antennae[antenna])):
                    one = self._antennae[antenna][i]
                    two = self._antennae[antenna][j]
                    v_dist = one[0] - two[0]
                    h_dist = one[1] - two[1]

                    for pair in [(one, 1), (two, -1)]:
                        multiple = 0
                        v_offset = v_dist * multiple
                        h_offset = h_dist * multiple
                        antinode = (pair[0][0] + (pair[1] * v_offset), pair[0][1] + (pair[1] * h_offset))
                        while self.is_valid(antinode):
                            antinodes.add(antinode)
                            multiple += 1
                            v_offset = v_dist * multiple
                            h_offset = h_dist * multiple
                            antinode = (pair[0][0] + (pair[1] * v_offset), pair[0][1] + (pair[1] * h_offset))


        return len(antinodes)

    def __str__(self):
        lines = []
        lines.append(f'height = {self._height}')
        lines.append(f'width = {self._width}')
        lines.append(f'antennae = {self._antennae}')
        return '\n'.join(lines)

def read_row(antenna_map, line):
    antenna_map.add_row(line.strip())

def main():
    antenna_map = AntennaMap()
    # util.read('day08/sample.txt', partial(read_row, antenna_map))
    util.read('day08/input.txt', partial(read_row, antenna_map))

    total = antenna_map.get_antinodes()
    print(f'total antinodes = {total}')

if __name__ == '__main__':
    main()
