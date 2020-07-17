#!/usr/bin/env python3
"""
Script which displays a pair plot
"""

import sys
import matplotlib.pyplot as plt

from describe import Data, Students, Features
from histogram import get_grades as get_grades_for_hist
from hogwarts import Gryffindor, Hufflepuff, Ravenclaw, Slytherin

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
        
        cls.gryffindor, cls.hufflepuff, cls.ravenclaw, cls.slytherin = \
            Gryffindor(), Hufflepuff(), Ravenclaw(), Slytherin()
        get_grades_for_hist(cls.courses, cls.gryffindor, cls.hufflepuff, cls.ravenclaw, cls.slytherin)

    @classmethod
    def pair(cls):
        ncourses = len(cls.courses)            
        fig, axs = plt.subplots(ncourses, ncourses, figsize=(15, 9))
        row = 0
        for course_y in cls.courses:
            col = 0
            for course_x in cls.courses:
                x, y = cls.grades[course_x], cls.grades[course_y]
                if (course_x == course_y):
                    cls.make_histogram(axs[row, col], course_x)
                else:
                    axs[row, col].scatter(x, y, s=1)
                axs[row, col].set_yticks([])
                axs[row, col].set_xticks([])
                col += 1
            row += 1
        cls.set_labels(fig, axs)

    @classmethod
    def make_histogram(cls, axs, course):
        for house in cls.gryffindor, cls.hufflepuff, cls.ravenclaw, cls.slytherin:
            axs.bar(0 + house.position, house.grades[course], color=house.color, width=1)


    @classmethod
    def set_labels(cls, fig, axs):
        fig.legend([0, 1, 2, 3],
                    labels=[
                        cls.gryffindor.name, cls.hufflepuff.name, 
                        cls.ravenclaw.name, cls.slytherin.name],
                    loc='lower left',
                    borderaxespad=0.1)

        row = 0
        for course in cls.courses:
            axs[row, 0].set_ylabel(course, rotation=30, ha='right')
            row += 1

        col = 0
        for course in cls.courses:
            axs[-1, col].set_xlabel(course, rotation=30, ha='right')
            col += 1
        

def main():
    assert len(sys.argv) == 2

    Data(sys.argv[1])
    if Students.nb == 0: raise ValueError

    Plot.get_courses()
    Plot.get_grades()
    Plot.pair()
    plt.subplots_adjust(top = 1, bottom = 0.15, right = 1, left = 0.15, 
        hspace = 0, wspace = 0)
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