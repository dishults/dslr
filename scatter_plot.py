#!/usr/bin/env python3
"""
Script which displays a scatter plot answering the next question:
What are the two features that are similar ?
"""

import sys
import matplotlib.pyplot as plt

from describe import Data, Students, Features
from hogwarts import Hogwarts, Gryffindor, Hufflepuff, Ravenclaw, Slytherin
from calculations import max_, min_, mean_, percentile_, sort_

class Plot():

    courses = []
    grades = {}

    @classmethod
    def get_courses(cls):
        cls.courses = Features.titles[6:]

    @classmethod
    def get_grades(cls):
        for course in cls.courses:
            course_nb = Features.titles.index(course)
            grades = Students.get_one_feature(course_nb)

            grades = [abs(grade) if grade != '' else 0 for grade in grades]

            max_grade = max_(grades)
            normalize = lambda grade: (grade * 100) // max_grade
            if (len(grades) > 100):
                grades = [percentile_(grades, p) for p in range(1, 100)]
            cls.grades[course] = [normalize(grade) for grade in grades if grade != 0]

    @classmethod
    def find_similar_features(cls, fig):
        c = 1
        for course_x in cls.courses:
            for course_y in cls.courses[c:]:
                diff = set(cls.grades[course_x]) - set(cls.grades[course_y])
                five_percent = (len(cls.grades[course_y]) * 5) // 100
                if len(diff) <= five_percent:
                    fig.suptitle(f"Two similar features:\n{course_x} - {course_y}")
                    return
            c += 1

    @classmethod
    def scatter(cls):
        i = 1
        for course in cls.courses:
            grades = cls.grades[course]
            position = [i] * len(grades)
            plt.scatter(position, list(grades))
            i += 1


def main():
    assert len(sys.argv) == 2

    Data(sys.argv[1])
    if Students.nb == 0: raise ValueError

    fig = plt.figure(figsize=(18, 7))

    Plot.get_courses()
    Plot.get_grades()
    Plot.scatter()
    Plot.find_similar_features(fig)

    plt.ylabel("Scores range", fontsize='large')
    plt.yticks([])
    plt.xticks(list(range(1, len(Plot.courses) + 1)), Plot.courses)
    fig.autofmt_xdate()
    plt.show()

if __name__ == "__main__":
    #try:
    main()
    #except AssertionError:
    #    print("Example usage: ./scatter_plot.py dataset_train.csv")
    #except (FileNotFoundError, StopIteration):
    #    print(f"Dataset file '{sys.argv[1]}' doesn't exist, is empty or incorrect")
    #except (IndexError, ValueError):
    #    print("Check that your dataset has all info about the student (6 first columns),\n"
    #          "at least two courses (starting from 7th column)\n"
    #          "and at least one student (row)")