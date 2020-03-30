#!/usr/bin/env python3

def all_nums(numbers):
    for number in numbers:
        if type(number) != int and type(number) != float:
            return False
    return True

def ceil_(number):
    return (1 - (number % 1)) + number

def len_(x):
    length = 0
    if type(x) == int or type(x) == float:
        while x >= 1:
            x /= 10
            length += 1
    else:
        for l in x:
            length += 1
    return length

def sum_(numbers):
    total = 0
    for number in numbers:
        total += number
    return total

#def round_(number, decimals=0):
#    multiplier = 10 ** decimals
#    return int(number * multiplier) / multiplier

def sort_(numbers):
    length = len_(numbers) - 1
    i = 0
    while i < length:
        if numbers[i] > numbers[i + 1]:
            swap = numbers[i]
            numbers[i] = numbers[i + 1]
            numbers[i + 1] = swap
            i = 0
        else:
            i += 1

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

def std_(numbers, mean=0):
    if mean == 0:
        mean = mean_(numbers)
    length = len_(numbers) - 1 #pandas like std, or remove -1 for numpy like
    return (sum_([(number - mean) ** 2 for number in numbers]) / length) ** 0.5

def min_(numbers):
    minimum = numbers[0]
    for number in numbers:
        if number < minimum:
            minimum = number
    return minimum

def percentile_(numbers, p):
    p /= 100
    length = len_(numbers)
    sort_(numbers)
    index = p * (length - 1)    #what number is at given % in numbers list
    if length % 2 == 0:         #if no middle -> index is always in between two values
        right_index = int(ceil_(index))
        left_index = right_index - 1
        right_proximity = index - left_index
        left_proximity = 1 - right_proximity
        right_weight = numbers[right_index] * right_proximity
        left_weight = numbers[left_index] * left_proximity
        return left_weight + right_weight
    else:
        return numbers[int(index)]

def max_(numbers):
    maximum = numbers[0]
    for number in numbers:
        if number > maximum:
            maximum = number
    return maximum
