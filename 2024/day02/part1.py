#! /usr/bin/env python

from common import util

from functools import partial
import re

def process_report(safe_reports, report):
    levels = [int(part) for part in re.split(r' +', report)]
    prev_level = None
    diff = None
    for level in levels:
        if prev_level is not None:
            new_diff = level - prev_level
            if abs(new_diff) < 1 or abs(new_diff) > 3:
                print(f'{report}: Unsafe (zero or too big)')
                return
            if (diff is not None) and ((diff < 0 and new_diff > 0) or (diff > 0 and new_diff < 0)):
                print(f'{report}: Unsafe (wrong direction)')
                return
            diff = new_diff
        prev_level = level

    print(f'{report}: Safe')
    safe_reports.append(report)

def main():
    safe_reports = []
    util.read('day2/input.txt', partial(process_report, safe_reports))

    print(f'num safe = {len(safe_reports)}')

if __name__ == '__main__':
    main()
