def num_len(x):
    length = 0
    while x >= 1:
        x /= 10
        length += 1
    return length

def sum_(numbers):
    total = 0
    for number in numbers:
        total += number
    return total

def sort_(numbers):
    try:
        length = len(numbers) - 1
        start = 0
        while start < length:
            smallest = min_(numbers[start:])
            i = start
            while numbers[i] != smallest:
                i += 1
            numbers[start], numbers[i] = numbers[i], numbers[start]
            start += 1
    except:
        pass

def count_(data, what=0):
    count = 0
    if what == 0:
        for d in data:
            if d or d == 0:
                count += 1
    elif what == 'numbers':
        for d in data:
            if type(d) == float or d == 0:
                count += 1
    return count

def mean_(numbers):
    s = sum_(numbers)
    l = len(numbers)
    if s != 0 and l != 0:
        return s / l
    return 0

def std_(numbers, mean=0):
    if mean == 0:
        mean = mean_(numbers)
    # Pandas-like std, or remove -1 for numpy-like
    length = len(numbers) - 1
    return (sum_([(number - mean) ** 2 for number in numbers]) / length) ** 0.5

def min_(numbers):
    try:
        minimum = numbers[0]
        for number in numbers:
            if number < minimum:
                minimum = number
        return minimum
    except:
        return numbers

def percentile_(numbers, p):
    p /= 100
    length = len(numbers)
    index = p * (length - 1)
    
    # If index is an int, a precise whole number => no need for guessing
    if index % 1 * 10 == 0: return numbers[int(index)]

    before = int(index)
    after = before + 1

    before_proximity = after - index
    after_proximity = 1 - before_proximity

    before_weight = numbers[before] * before_proximity
    after_weight = numbers[after] * after_proximity

    return before_weight + after_weight

def max_(numbers):
    maximum = numbers[0]
    for number in numbers:
        if number > maximum:
            maximum = number
    return maximum
