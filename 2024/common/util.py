#! /usr/bin/env python

def read(filename, line_processor):
    with open(filename, mode='r') as f:
        for line in f:
            line_processor(line.strip())
