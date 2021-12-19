#! /usr/bin/env python

import sys


class Target:
    def __init__(self, x0, x1, y0, y1):
        if x0 >= x1:
            x0, x1 = x1, x0
        if y0 >= y1:
            y0, y1 = y1, y0
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

    def __str__(self):
        return 'x({}, {}), y({}, {})'.format(self.x0, self.x1, self.y0,
                                             self.y1)

    def in_target(self, x, y):
        if x < self.x0 or x > self.x1 or y < self.y0 or y > self.y1:
            return False
        return True

    def in_x_range(self, x):
        return self.x0 <= x and x <= self.x1

    def in_y_range(self, y):
        return self.y0 <= y and y <= self.y1


def step_probe(pos, vel):
    pos[0] += vel[0]
    pos[1] += vel[1]
    if vel[0] > 0:
        vel[0] -= 1
    elif vel[0] < 0:
        vel[0] += 1
    vel[1] -= 1


def get_steps(vel_x, target):
    pos = [0, 0]
    vel = [vel_x, 0]
    possible_step_nums = []
    i = 0
    while vel[0] > 0 and pos[1] <= target.x1:
        step_probe(pos, vel)
        i += 1
        if target.in_x_range(pos[0]):
            possible_step_nums.append(i)
    dropping = target.in_x_range(pos[0])

    return (possible_step_nums, dropping)


def get_possible_y(target, step_num):
    pos = [0, 0]
    possible_y_vel = []

    possible_y = target.y0
    vel = [0, possible_y]
    for i in range(step_num):
        step_probe(pos, vel)
    if target.in_y_range(pos[1]):
        possible_y_vel.append(possible_y)

    while pos[1] <= target.y1:
        possible_y += 1
        pos = [0, 0]
        vel = [0, possible_y]
        for i in range(step_num):
            step_probe(pos, vel)
        if target.in_y_range(pos[1]):
            possible_y_vel.append(possible_y)

    return possible_y_vel


def get_drop_steps(target, num_steps):
    drop_steps = []
    min_steps = 2 * int(num_steps / 2) + 1
    pos = [0, 0]
    start_y_vel = -(int(min_steps / 2) + 1)
    vel = [0, start_y_vel]
    while start_y_vel >= target.y0:
        extra_steps = 0
        while pos[1] > target.y1:
            step_probe(pos, vel)
            extra_steps += 1
            if target.in_y_range(pos[1]):
                drop_steps.append((min_steps + extra_steps, int(num_steps / 2),
                                   -start_y_vel - 1))
        start_y_vel -= 1
        vel = [0, start_y_vel]
        pos = [0, 0]

    return drop_steps


def get_max_y(y):
    if y <= 0:
        return 0
    return int(y * (y + 1) / 2)


def main(args):
    targets = []
    with open(args[0], 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().replace('target area: ', '')
            parts = line.split(', ')
            parts[0] = parts[0].replace('x=', '')
            x_parts = [int(x) for x in parts[0].split('..')]
            parts[1] = parts[1].replace('y=', '')
            y_parts = [int(y) for y in parts[1].split('..')]
            targets.append(
                Target(x_parts[0], x_parts[1], y_parts[0], y_parts[1]))

    for target in targets:
        possible_x = {}
        possible_step_nums = set()
        possible_drop = False
        for x in range(1, target.x1 + 1):
            pos = [0, 0]
            (steps, dropping) = get_steps(x, target)
            if len(steps) > 0:
                possible_x[x] = (steps, dropping)
                possible_drop = possible_drop or dropping
                for step_num in steps:
                    possible_step_nums.add(step_num)

        possible_y = {}
        for step_num in possible_step_nums:
            y_vels = get_possible_y(target, step_num)
            possible_y[step_num] = y_vels

        max_y = None
        for step in possible_y:
            for y in possible_y[step]:
                height = get_max_y(y)
                if max_y is None or height > max_y:
                    max_y = height
        if possible_drop:
            for x in possible_x:
                (steps, dropping) = possible_x[x]
                if dropping:
                    drop_steps = get_drop_steps(target, steps[-1])
                    max_y_vel = max([z for (x, y, z) in drop_steps])
                    height = get_max_y(max_y_vel)
                    if max_y is None or height > max_y:
                        max_y = height
        print('final max_y = {}'.format(max_y))


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
