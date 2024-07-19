#!/usr/bin/env python

import sys

current_word = None
current_count = 0

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # parse the input we got from mapper.py
    word, count = line.split("\t", 1)
    # convert count to int
    count = int(count)
    
    # key is the same as before
    if current_word == word:
        current_count += count
    else:
        # new word encountered
        if current_word:
            print(f"{current_word}\t{current_count}")
        current_word = word
        current_count = count

# output the last word
if current_word == word:
    print(f"{current_word}\t{current_count}")
