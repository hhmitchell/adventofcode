#! /usr/bin/env python

from common import util

from functools import partial
from itertools import chain
import re

def read_row(rows, row):
    rows.append(row.strip())

def check(rows, i, j):
    if rows[i][j] != 'A':
        return 0

    if (((rows[i - 1][j - 1] == 'M' and rows[i + 1][j + 1] == 'S') or
         (rows[i - 1][j - 1] == 'S' and rows[i + 1][j + 1] == 'M')) and
        ((rows[i - 1][j + 1] == 'M' and rows[i + 1][j - 1] == 'S') or
         (rows[i - 1][j + 1] == 'S' and rows[i + 1][j - 1] == 'M'))):
       return 1

    return 0

def main():
    rows = []
    util.read('day4/input.txt', partial(read_row, rows))
    assert all([len(rows[i]) == len(rows[0]) for i in range(1, len(rows))])

    total = 0
    for i in range(1, len(rows) - 1):
        for j in range(1, len(rows[i]) - 1):
            total += check(rows, i, j)

    print(f'total = {total}')

if __name__ == '__main__':
    main()
