#!/usr/bin/env python3

import numpy as np #tmp

def sum_(numbers):
    total = 0
    for number in numbers:
        total += number
    return total

def len_(x):
    length = 0
    for l in x:
        length += 1
    return length

def all_nums(numbers):
    for number in numbers:
        if type(number) != int and type(number) != float:
            return False
    return True

def count_(data):
    count = 0
    for d in data:
        if d:
            count += 1
    return count

def mean_(numbers):
    if all_nums(numbers):
        s = sum_(numbers)
        l = len_(numbers)
        if s > 0 and l > 0:
            return s / l
    return 0

def min_(numbers):
    minimum = numbers[0]
    for number in numbers:
        if number < minimum:
            minimum = number
    return minimum

def percentile_(numbers, p):
    p /= 100
    length = len_(numbers)
    numbers.sort() #to-do
    index = p * (length - 1)    #what number is at given % in numbers list
    if length % 2 == 0:         #if no middle -> index is always in between two values
        right_index = int(np.ceil(index)) #to-do
        left_index = right_index - 1
        right_proximity = index - left_index
        left_proximity = 1 - right_proximity
        right_weight = numbers[right_index] * right_proximity
        left_weight = numbers[left_index] * left_proximity
        #print(f"{p}% \t {index} \t {left_index} / {right_index} ") #tmp
        return left_weight + right_weight
    else:
        return numbers[int(index)]

def max_(numbers):
    maximum = numbers[0]
    for number in numbers:
        if number > maximum:
            maximum = number
    return maximum

#def test(xx):
#    for x in xx:
#        print('\n', x)
#        print(f'25%: {percentile_(x, 25)} - {np.percentile(np.array(x), 25)}\n'
#            f'50%: {percentile_(x, 50)} - {np.percentile(np.array(x), 50)}\n'
#            f'75%: {percentile_(x, 75)} - {np.percentile(np.array(x), 75)}')

#x1 = [1, 2, 3, 4]
#x2 = [2, 3, 4, 5]
#x11 = [4, 2, 1, 7]
#x3 = [1, 2, 3, 4, 5]
#x4 = [4, 2, 3, 11, 8]
#test([x1, x2, x11, x3, x4])