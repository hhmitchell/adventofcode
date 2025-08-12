#! /usr/bin/env python

from common import util

from functools import partial
import re

class Point():
    def __init__(self, row, col):
        self._row = row
        self._col = col

    def row(self):
        return self._row

    def col(self):
        return self._col

    def __repr__(self):
        return f'({self._row}, {self._col})'

    def __eq__(self, other):
        return other.row() == self.row() and other.col() == self.col()

    def __hash__(self):
        return (self._row, self._col).__hash__()

class TopoMap():
    def __init__(self):
        self._map = []
        self._trailheads = []

    def score(self, point):
        return self._map[point.row()][point.col()]

    def add_row(self, row):
        for match in re.finditer(r'0', row):
            self._trailheads.append(Point(len(self._map), match.start()))
        self._map.append([int(char) for char in row])

    def width(self):
        return len(self._map[0])

    def height(self):
        return len(self._map)

    def find_peaks(self, point):
        score = self.score(point)
        # print(f'find peaks for {point} with score {score}')
        if score == 9:
            # print(f'returning peak: {point}')
            return set([point])

        peaks = set()
        row = point.row()
        col = point.col()
        if row > 0:
            if self._map[row - 1][col] == score + 1:
                peaks = peaks.union(self.find_peaks(Point(row - 1, col)))
        if row < self.height() - 1:
            if self._map[row + 1][col] == score + 1:
                peaks = peaks.union(self.find_peaks(Point(row + 1, col)))
        if col > 0:
            if self._map[row][col - 1] == score + 1:
                peaks = peaks.union(self.find_peaks(Point(row, col - 1)))
        if col < self.width() - 1:
            if self._map[row][col + 1] == score + 1:
                peaks = peaks.union(self.find_peaks(Point(row, col + 1)))

        # print(f'returning peaks: {peaks}')
        return peaks

    def get_score(self):
        score = 0
        for trailhead in self._trailheads:
            peaks = self.find_peaks(trailhead)
            # print(f'for trailhead {trailhead}, got peaks {peaks}')
            score += len(peaks)

        return score


    def __repr__(self):
        lines = []
        lines.append(repr(self._map))
        lines.append(repr(self._trailheads))
        return '\n'.join(lines)

def process_line(topo_map, line):
    topo_map.add_row(line.strip())

def main():
    topo_map = TopoMap()
    # util.read('day10/sample.txt', partial(process_line, topo_map))
    util.read('day10/input.txt', partial(process_line, topo_map))

    print(f'{topo_map}')
    print(f'total score = {topo_map.get_score()}')

if __name__ == '__main__':
    main()
