#! /usr/bin/env python

import itertools
import sys

DIGITS = [
    'abcefg',
    'cf',
    'acdeg',
    'acdfg',
    'bcdf',
    'abdfg',
    'abdefg',
    'acf',
    'abcdefg',
    'abcdfg',
]
SEGMENTS = []
DIGIT_TO_VALUE = {}
for i in range(len(DIGITS)):
    digit = DIGITS[i]
    SEGMENTS.extend(list(digit))
    DIGIT_TO_VALUE[digit] = i
SEGMENTS = frozenset(SEGMENTS)


def create_possible_mappings(segments):
    mappings = []
    for permutation in itertools.permutations(segments):
        mappings.append(dict(zip(segments, permutation)))

    return mappings


def decode(patterns, values):
    decoded_values = []
    for mapping in create_possible_mappings(SEGMENTS):
        matched = True
        for pattern in patterns:
            segments = []
            for char in pattern:
                segments.append(mapping[char])
            digit = ''.join(sorted(segments))

            if digit not in DIGIT_TO_VALUE:
                matched = False
                continue

        if not matched:
            continue

        decoded_value = ''
        for value in values:
            segments = []
            for char in value:
                segments.append(mapping[char])
            decoded_value += str(DIGIT_TO_VALUE[''.join(sorted(segments))])
        decoded_values.append(int(decoded_value))

    return decoded_values


def main(args):
    decoded_values = []
    with open(args[0], 'r') as f:
        for line in f.readlines():
            parts = line.strip().split(' | ')
            patterns = parts[0].split()
            values = parts[1].split()

            decoded_values.extend(decode(patterns, values))

    print(sum(decoded_values))


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
