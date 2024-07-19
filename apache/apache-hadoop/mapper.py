#!/usr/bin/env python

import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    words = line.split()
    # output key-value pairs to STDOUT (standard output)
    for word in words:
        print(f"{word}\t1")
