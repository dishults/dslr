#!/usr/bin/env python3
"""
Script which displays a histogram answering the next question:
Which Hogwarts course has a homogeneous score distribution
between all four houses?
"""

import sys
import matplotlib.pyplot as plt

import my_exceptions as error

from describe import Data, Students, Features
from hogwarts import Hogwarts, Gryffindor, Hufflepuff, Ravenclaw, Slytherin

def get_grades(courses, gryffindor, hufflepuff, ravenclaw, slytherin):
    for course in courses:
        for house in gryffindor, hufflepuff, ravenclaw, slytherin:
            house.get_grades(course)
    
    Features.analyze(depth=0)
    for course in courses:
        Hogwarts.normalize_grades(course)

def plot(courses, gryffindor, hufflepuff, ravenclaw, slytherin):
    for house in gryffindor, hufflepuff, ravenclaw, slytherin:
        house.set_label(courses[0])
    position = 5
    
    for course in courses[1:]:
        for house in gryffindor, hufflepuff, ravenclaw, slytherin:
            house.plot(position, house.grades[course])
        position += 5
        plt.bar(position, 0, width=0)

def make_histogram(courses):
    fig = plt.figure(figsize=(18, 7))
    fig.suptitle("Courses")
    plt.ylabel("Scores range", fontsize='large')
    yield
    plt.yticks([])
    plt.xticks(list(range(4, len(courses) * 5, 5)), courses)
    fig.autofmt_xdate()
    plt.legend()
    plt.show()
    yield

def main():
    if len(sys.argv) != 2: raise error.Usage
    Data(sys.argv[1], fix_grades=True)

    gryffindor, hufflepuff, ravenclaw, slytherin = \
        Gryffindor(), Hufflepuff(), Ravenclaw(), Slytherin()

    courses = Features.titles[6:]
    histogram = make_histogram(courses)
    next(histogram)

    get_grades(courses, gryffindor, hufflepuff, ravenclaw, slytherin)
    plot(courses, gryffindor, hufflepuff, ravenclaw, slytherin)
    next(histogram)


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, StopIteration):
        raise error.File
    except (IndexError, ValueError):
        raise error.Dataset
