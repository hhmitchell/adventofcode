#! /usr/bin/env python

from common import util

from functools import partial
import re

class Rules():
    def __init__(self):
        self._children = {}

    def add_rule(self, rule):
        x = rule[0]
        y = rule[1]
        if x not in self._children:
            self._children[x] = set()
        self._children[x].add(y)

    def reset(self):
        self._temp_children = self._children.copy()
        self._temp_printed_pages = set()

    def check_page(self, page):
        if page in self._temp_children:
            if len(self._temp_children[page]):
                common = self._temp_children[page].intersection(self._temp_printed_pages)
                if common:
                    return False

        self._temp_printed_pages.add(page)
        return True


def read_row(rules, valid_middles, row):
    content = row.strip()
    if read_row.read_rules:
        if content:
            rules.add_rule(content.split('|'))
        else:
            read_row.read_rules = False
    else:
        update = content.split(',')
        middle = get_valid_middle(rules, update)
        if middle is not None:
            valid_middles.append(middle)

read_row.read_rules = True

def get_valid_middle(rules, update):
    assert(len(update) % 2 == 1)

    rules.reset()
    for page in update:
        if not rules.check_page(page):
            return None
    return update[int(len(update)/2)]

def main():
    rules = Rules()
    valid_middles = []
    util.read('day5/input.txt', partial(read_row, rules, valid_middles))

    print(f'total = {sum([int(x) for x in valid_middles])}')

if __name__ == '__main__':
    main()
