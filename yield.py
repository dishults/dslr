#!/usr/bin/env python3

def func(some_stuff):
    x = 0
    while x < 10:
        x += 1
        yield x

f = list(func(2))
print(f)