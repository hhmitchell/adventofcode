#! /usr/bin/env python

from common import util

from functools import partial
import re

def process_line(test_values, line):
    parts = line.strip().split(':')
    target = int(parts[0].strip())
    operands = [int(val.strip()) for val in parts[1].split()]

    operators = '+*'
    permutations = pow(len(operators), len(operands) - 1)
    for i in range(permutations):
        total = operands[0]
        index = 1
        while total <= target and index < len(operands):
            operator = operators[i & 1]
            operand = operands[index]
            if operator == '+':
                total += operand
            else:
                total *= operand
            i >>= 1
            index += 1
        if total == target:
            test_values.append(target)
            return

def main():
    test_values = []
    util.read('day07/input.txt', partial(process_line, test_values))

    print(f'total = {sum(test_values)}')

if __name__ == '__main__':
    main()
