#!/usr/bin/env python3
"""
Script which displays a pair plot
"""

import sys
import matplotlib.pyplot as plt

from describe import Data, Students, Features
import numpy as np

class Plot:

    courses = ()
    grades = {}

    @classmethod
    def get_courses(cls):
        cls.courses = Features.titles[6:]

    @classmethod
    def get_grades(cls):
        for course in cls.courses:
            course_nb = Features.titles.index(course)
            grades = Students.get_one_feature(course_nb)
            cls.grades[course] = [grade if grade != '' else 0 for grade in grades]

    @classmethod
    def scatter(cls):
        ncourses = len(cls.courses)
        npairs = ncourses * (ncourses - 1) // 2
        print("npairs: ", npairs)
        nrows = npairs ** 0.5
        if nrows % 1 > 0:
            nrows = int(nrows)
            ncols = npairs / nrows
            if ncols % 1 > 0:
                ncols += 1
            ncols = int(ncols)
        else:
            ncols = int(nrows)
            
        #print("size: ", nrows, ncols)
        fig, axs = plt.subplots(nrows, ncols, figsize=(15, 10))
        fig.suptitle("Courses pairs")
        c = 1
        row = 0
        col = 0
        for course_x in cls.courses:
            for course_y in cls.courses[c:]:
                x = cls.grades[course_x]
                y = cls.grades[course_y]

                axs[row, col].plot(x, y)

                axs[row, col].set_ylabel(course_y)
                axs[row, col].set_xlabel(course_x)
                axs[row, col].set_yticks([])
                axs[row, col].set_xticks([])

                #print(row, col)
                col += 1
                if col == ncols:
                    row += 1
                    col = 0
            c += 1


def main():
    assert len(sys.argv) == 2

    Data(sys.argv[1])
    if Students.nb == 0: raise ValueError

    Plot.get_courses()
    Plot.get_grades()
    Plot.scatter()
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