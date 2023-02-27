#!/usr/bin/env python3
cycle = 0

def incr_cycle():
    global cycle
    # if cycle%1000 == 0:
    #     print(cycle)
    cycle += 1

def get_cycle():
    global cycle
    return cycle
