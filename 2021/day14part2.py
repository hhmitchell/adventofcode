#! /usr/bin/env python

import re
import sys


def add_to_count_map(count_map, key, count=1):
    if key not in count_map:
        count_map[key] = 0
    count_map[key] += count


def main(args):
    template = None
    rules = {}
    with open(args[0], 'r') as f:
        lines = f.readlines()
        template = lines[0].strip()
        for line in lines[2:]:
            parts = line.strip().split(' -> ')
            rules[tuple(list(parts[0]))] = parts[1]

    polymer = {}
    for i in range(len(template) - 1):
        pair = (template[i], template[i + 1])
        add_to_count_map(polymer, pair)

    num_steps = 40
    for i in range(num_steps):
        new_polymer = {}
        for pair in polymer:
            add_to_count_map(new_polymer, (pair[0], rules[pair]),
                             polymer[pair])
            add_to_count_map(new_polymer, (rules[pair], pair[1]),
                             polymer[pair])
        polymer = new_polymer

    count_map = {}
    for pair in polymer:
        add_to_count_map(count_map, pair[0], polymer[pair])
    add_to_count_map(count_map, template[-1])

    counts = sorted((count_map[k], k) for k in count_map)
    print(counts[-1][0] - counts[0][0])


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
