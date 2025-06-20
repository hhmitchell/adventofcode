#! /usr/bin/env python

from common import util

from functools import partial
import re

def parse_report(report):
    return [int(part) for part in re.split(r' +', report)]

def is_safe(levels):
    if ((not all(levels[i] == sorted(levels)[i] for i in range(len(levels)))) and
       (not all(levels[i] == sorted(levels, reverse=True)[i] for i in range(len(levels))))):
        return False
    if not all(abs(levels[i] - levels[i + 1]) > 0 and abs(levels[i] - levels[i + 1]) < 4 for i in range(len(levels) - 1)):
        return False

    return True

def process_report(safe_reports, report):
    levels = parse_report(report)
    if is_safe(levels):
        safe_reports.append(levels)
        return

    for i in range(len(levels)):
        if is_safe(levels[0:i] + levels[i + 1:]):
            safe_reports.append(levels)
            return

def main():
    safe_reports = []
    util.read('day2/input.txt', partial(process_report, safe_reports))

    print(f'num safe = {len(safe_reports)}')

if __name__ == '__main__':
    main()
