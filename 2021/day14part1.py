#! /usr/bin/env python

import re
import sys


def main(args):
    template = None
    rules = {}
    with open(args[0], 'r') as f:
        lines = f.readlines()
        template = lines[0].strip()
        for line in lines[2:]:
            parts = line.strip().split(' -> ')
            rules[tuple(list(parts[0]))] = parts[1]

    polymer = list(template)
    num_steps = 10
    for i in range(num_steps):
        new_elements = []
        for j in range(len(polymer) - 1):
            new_elements.append(rules[(polymer[j], polymer[j + 1])])
        new_polymer = [None] * (len(polymer) + len(new_elements))
        new_polymer[::2] = polymer
        new_polymer[1::2] = new_elements
        polymer = new_polymer

    count_map = {}
    for element in polymer:
        if element not in count_map:
            count_map[element] = 0
        count_map[element] += 1

    counts = sorted((count_map[k], k) for k in count_map)
    print(counts[-1][0] - counts[0][0])


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
