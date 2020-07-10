#!/usr/bin/env python3
"""
Script which displays a histogram answering the next question:
Which Hogwarts course has a homogeneous score distribution
between all four houses?
"""

import sys
import matplotlib.pyplot as plt

from describe import Data, Students, Features
from hogwarts import Gryffindor, Hufflepuff, Ravenclaw, Slytherin

def get_grades(courses, g, h, r, s):
    for course in courses:
        g.get_grades(course)
        h.get_grades(course)
        r.get_grades(course)
        s.get_grades(course)

def set_labels(course, g, h, r, s):
    g.set_label(course)
    h.set_label(course)
    r.set_label(course)
    s.set_label(course)

def plot(courses, g, h, r, s):
    position = 5

    for course in courses:
        g.plot(position, g.grades[course])
        h.plot(position, h.grades[course])
        r.plot(position, r.grades[course])
        s.plot(position, s.grades[course])
        plt.bar(position + 5, 0, width=0)
        position += 5

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
    assert len(sys.argv) == 2

    Data(sys.argv[1])
    if Students.nb == 0:
        raise ValueError
        
    g = Gryffindor()
    h = Hufflepuff()
    r = Ravenclaw()
    s = Slytherin()

    courses = Features.titles[6:]
    histogram = make_histogram(courses)
    next(histogram)

    get_grades(courses, g, h, r, s)
    set_labels(courses[0], g, h, r, s)
    plot(courses[1:], g, h, r, s)
    next(histogram)


if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        print("Example usage: ./histogram.py dataset_train.csv")
    except (StopIteration, IndexError, ValueError):
        print("Check that your table isn't empty.\n"
              "That it has all info about the student (6 first columns),\n"
              "at least one course (starting from 7th column)\n"
              "and at least one student (row)")
