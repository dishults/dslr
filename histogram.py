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
from DSCRB.calculations import min_

def get_grades(courses, gryffindor, hufflepuff, ravenclaw, slytherin):
    Features.analyze(depth=1)
    Students.fix_empty_grades()
    for course in courses:
        for house in gryffindor, hufflepuff, ravenclaw, slytherin:
            house.get_grades(course, std_diff=True)
    
def show_all_histograms(axs, courses, gryffindor, hufflepuff, ravenclaw, slytherin):
    for course_nb, course in enumerate(courses):
        for house in gryffindor, hufflepuff, ravenclaw, slytherin:
            house.hist(course, axs[course_nb])

def make_histogram(courses, gryffindor, hufflepuff, ravenclaw, slytherin):
    fig, axs = plt.subplots(1, len(courses), figsize=(16, 4),
                            subplot_kw={"box_aspect":1})
    fig.suptitle("Grades for courses")
    axs[0].set_ylabel("Number of students", fontsize='large')
    yield axs
    for col, course in enumerate(courses):
        axs[col].set_xlabel(course, rotation=30, ha='right')
        axs[col].set_yticks([]), axs[col].set_xticks([])
    fig.legend([gryffindor.name, hufflepuff.name,
                ravenclaw.name, slytherin.name],
                loc='lower left', borderaxespad=0.1)
    plt.subplots_adjust(top=1, bottom=0.15, left=0.03, right=1, wspace=0)
    plt.show()
    yield

def find_homogeneous_course(courses, gryffindor, hufflepuff, ravenclaw, slytherin):
    total_diff = []
    for course in courses:
        diff = 0
        for house in gryffindor, hufflepuff, ravenclaw, slytherin:
            diff += abs(house.std_diff[course])
        total_diff.append(diff)
    
    found = total_diff.index(min_(total_diff))
    for house in gryffindor, hufflepuff, ravenclaw, slytherin:
        house.hist(courses[found])

    plt.title(f"Most homogeneous Hogwarts course:\n{courses[found]}")
    plt.ylabel("Number of students")
    plt.xlabel("Grades")
    plt.show()

def main():
    if len(sys.argv) != 2: raise error.Usage
    Data(sys.argv[1], check_houses=True)

    gryffindor, hufflepuff, ravenclaw, slytherin = \
        Gryffindor(), Hufflepuff(), Ravenclaw(), Slytherin()

    courses = Features.titles[6:]
    histogram = make_histogram(courses, gryffindor, hufflepuff, ravenclaw, slytherin)
    axs = next(histogram)

    get_grades(courses, gryffindor, hufflepuff, ravenclaw, slytherin)
    show_all_histograms(axs, courses, gryffindor, hufflepuff, ravenclaw, slytherin)
    next(histogram)
    find_homogeneous_course(courses, gryffindor, hufflepuff, ravenclaw, slytherin)

if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, StopIteration):
        raise error.File
    except (IndexError, ValueError, KeyError, TypeError):
        raise error.Dataset
