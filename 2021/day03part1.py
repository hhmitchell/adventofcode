#! /usr/bin/env python

import sys


def main(args):
    num_bits = None
    num_ones = []
    num_values = 0
    with open(args[0], 'r') as f:
        lines = f.readlines()
        num_values = len(lines)
        for line in lines:
            value = line.strip()
            if num_bits is None:
                num_bits = len(value)
                num_ones = [0] * num_bits
            elif len(value) != num_bits:
                print('Input error!')
            value = int(value, 2)
            for i in range(num_bits):
                if value & 1 == 1:
                    num_ones[i] += 1
                value = value >> 1

    gamma = 0
    for i in range(num_bits):
        num = num_ones[num_bits - i - 1]
        gamma = gamma << 1
        gamma |= (1 if num > num_values - num else 0)
    epsilon = ~gamma & (pow(2, num_bits) - 1)

    print(gamma * epsilon)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
