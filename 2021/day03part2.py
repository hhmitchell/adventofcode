#! /usr/bin/env python

import sys


def process_list(values, bit_pos, bit_value):
    results = ([], [])
    for value in values:
        results[int(value[bit_pos])].append(value)

    if bit_value == 0:
        return results[0] if len(results[0]) <= len(results[1]) else results[1]
    else:
        return results[1] if len(results[1]) >= len(results[0]) else results[0]


def main(args):
    all_values = []
    with open(args[0], 'r') as f:
        lines = f.readlines()
        all_values = [line.strip() for line in lines]

    oxygen = all_values
    co2_scrubber = all_values
    bit_pos = 0
    while len(oxygen) > 1 or len(co2_scrubber) > 1:
        if len(oxygen) > 1:
            oxygen = process_list(oxygen, bit_pos, 1)
        if len(co2_scrubber) > 1:
            co2_scrubber = process_list(co2_scrubber, bit_pos, 0)
        bit_pos += 1

    print(int(oxygen[0], 2) * int(co2_scrubber[0], 2))


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
