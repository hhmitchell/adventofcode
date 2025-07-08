#! /usr/bin/env python

from common import util

from functools import partial
import re

def read_row(rows, row):
    rows.append(row.strip())

def make_up_diags(rows):
    diags = []
    for z in range(len(rows)):
        chars = []
        for i in range(z, -1, -1):
            j = z - i
            chars.append(rows[i][j])
        diags.append(''.join(chars))

    for z in range(1, len(rows[0])):
        chars = []
        for i in range(len(rows) - 1, z - 1, -1):
            j = len(rows) - i + z - 1
            chars.append(rows[i][j])
        diags.append(''.join(chars))

    return diags

def make_down_diags(rows):
    diags = []
    for z in range(len(rows)):
        chars = []
        for i in range(z, len(rows)):
            j = i - z
            chars.append(rows[i][j])
        diags.append(''.join(chars))

    for z in range(1, len(rows[0])):
        chars = []
        for i in range(0, len(rows[0]) - z):
            j = z + i
            chars.append(rows[i][j])
        diags.append(''.join(chars))

    return diags


def main():
    word = 'XMAS'
    rows = []
    util.read('day4/input.txt', partial(read_row, rows))
    assert all([len(rows[i]) == len(rows[0]) for i in range(1, len(rows))])
    columns = [''.join(col) for col in zip(*rows)]
    up_diags = make_up_diags(rows)
    down_diags = make_down_diags(rows)

    total = 0
    for strings in [rows, columns, up_diags, down_diags]:
        total += sum(len(re.findall(word, string)) for string in strings)
        total += sum(len(re.findall(word[::-1], string)) for string in strings)
    print(f'total = {total}')

if __name__ == '__main__':
    main()
