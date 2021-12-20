#! /usr/bin/env python

import ast
import sys


def is_iterable(n):
    try:
        _ = iter(n)
        return True
    except TypeError as te:
        return False


class Number:
    def __init__(self, n, parent=None):
        if not is_iterable(n):
            raise Exception('{} is not iterable'.format(n))
        if len(n) != 2:
            raise Exception('{} must have length 2.')

        self.parent = parent
        self.depth = self.parent.depth + 1 if self.parent else 0

        if is_iterable(n[0]):
            self.l_number = Number(n[0], self)
            self.l_value = None
        else:
            self.l_number = None
            self.l_value = n[0]
        if is_iterable(n[1]):
            self.r_number = Number(n[1], self)
            self.r_value = None
        else:
            self.r_number = None
            self.r_value = n[1]

    def __add__(self, value):
        sum = Number([self.to_list(), value.to_list()])
        while True:
            x = sum.get_explodable()
            if x:
                x.explode()
                continue
            x = sum.get_splittable()
            if x:
                x.split()
                continue
            break
        return sum

    def __str__(self):
        return str(self.to_list())

    def debug_str(self):
        lines = []
        return '({}{}, {})'.format(
            self.__annotation(),
            self.l_number.debug_str()
            if self.l_number else '{}'.format(self.l_value),
            self.r_number.debug_str()
            if self.r_number else '{}'.format(self.r_value))

    def __annotation(self):
        parts = []
        if self.l_number is None and self.r_number is None:
            parts.append('d={}'.format(self.depth))
        if self.is_explodable():
            parts.append('E')
        if self.is_splittable():
            parts.append('S')
        return ' '.join(parts) + '; ' if len(parts) else ''

    def to_list(self):
        result = [None, None]
        result[0] = self.l_number.to_list() if self.l_number else self.l_value
        result[1] = self.r_number.to_list() if self.r_number else self.r_value
        return result

    def is_explodable(self):
        return False if self.l_number or self.r_number else self.depth >= 4

    def get_explodable(self):
        if self.is_explodable():
            return self
        else:
            if self.l_number:
                result = self.l_number.get_explodable()
                if result:
                    return result
            if self.r_number:
                return self.r_number.get_explodable()

    def explode(self):
        if not self.is_explodable():
            return
        if self.parent:
            self.parent.add_left(self.l_value, self, True)
            self.parent.add_right(self.r_value, self, True)
        self.parent.replace(self, 0)

    def add_left(self, value, source, upwards):
        if upwards:
            if self.l_number == source:
                if self.parent:
                    self.parent.add_left(value, self, True)
                else:
                    pass
            elif self.r_number == source:
                if self.l_number:
                    self.l_number.add_left(value, self, False)
                else:
                    self.l_value += value

            else:
                raise Exception('wut')
        else:
            if self.r_number:
                self.r_number.add_left(value, self, False)
            else:
                self.r_value += value

    def add_right(self, value, source, upwards):
        if upwards:
            if self.r_number == source:
                if self.parent:
                    self.parent.add_right(value, self, True)
                else:
                    pass
            elif self.l_number == source:
                if self.r_number:
                    self.r_number.add_right(value, self, False)
                else:
                    self.r_value += value

            else:
                raise Exception('wut')
        else:
            if self.l_number:
                self.l_number.add_right(value, self, False)
            else:
                self.l_value += value

    def replace(self, number, value):
        if self.l_number == number:
            self.l_number = None
            self.l_value = value
        if self.r_number == number:
            self.r_number = None
            self.r_value = value

    def is_splittable(self):
        return self.is_left_splittable() or self.is_right_splittable()

    def is_left_splittable(self):
        return not self.l_number and self.l_value >= 10

    def is_right_splittable(self):
        return not self.r_number and self.r_value >= 10

    def get_splittable(self):
        padding = '  ' * self.depth
        if self.is_left_splittable():
            return self
        elif self.l_number:
            result = self.l_number.get_splittable()
            if result:
                return result

        if self.is_right_splittable():
            return self
        elif self.r_number:
            return self.r_number.get_splittable()

    def split(self):
        if self.is_left_splittable():
            self.l_number = Number(
                [int(self.l_value / 2),
                 int((self.l_value + 1) / 2)], self)
            return
        if self.is_right_splittable():
            self.r_number = Number(
                [int(self.r_value / 2),
                 int((self.r_value + 1) / 2)], self)

    def magnitude(self):
        result = 3 * (self.l_number.magnitude() if self.l_number else
                      self.l_value) + 2 * (self.r_number.magnitude()
                                           if self.r_number else self.r_value)
        return result


def main(args):
    numbers = []
    with open(args[0], 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        for line in lines:
            if line[0] != '#':
                numbers.append(Number(ast.literal_eval(line)))

    sum = numbers[0]
    for n in numbers[1:]:
        sum += n
    print(sum)
    print(sum.magnitude())


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
