#!/usr/bin/env python3
"""
Script which displays a pair plot
"""

import sys
import matplotlib.pyplot as plt

from describe import Data, Students, Features
from histogram import get_grades as get_grades_for_histogram
from hogwarts import Hogwarts, Gryffindor, Hufflepuff, Ravenclaw, Slytherin

class Plot:

    courses = ()
    grades = {}

    @classmethod
    def get_courses(cls):
        cls.courses = Features.titles[6:]

    @classmethod
    def get_grades(cls):        
        cls.gryffindor, cls.hufflepuff, cls.ravenclaw, cls.slytherin = \
            Gryffindor(), Hufflepuff(), Ravenclaw(), Slytherin()

        get_grades_for_histogram(cls.courses, 
                                cls.gryffindor, cls.hufflepuff, 
                                cls.ravenclaw, cls.slytherin)

        for house in cls.gryffindor, cls.hufflepuff, cls.ravenclaw, cls.slytherin:
            house.raw_grades = {}
        for course in cls.courses:
            for house in cls.gryffindor, cls.hufflepuff, cls.ravenclaw, cls.slytherin:
                house.raw_grades[course] = Hogwarts.get_grades(house, course)

    @classmethod
    def pair(cls):
        course_nb = len(cls.courses)            
        fig, axs = plt.subplots(course_nb, course_nb, figsize=(15, 9))
        row = 0
        for course_y in cls.courses:
            col = 0
            for course_x in cls.courses:
                if (course_x == course_y):
                    cls.make_histogram(axs[row, col], course_x)
                else:
                    cls.make_scatter_plot(axs[row, col], course_x, course_y)
                axs[row, col].set_yticks([])
                axs[row, col].set_xticks([])
                col += 1
            row += 1
        cls.set_labels(fig, axs)

    @classmethod
    def make_histogram(cls, axs, course):
        for house in cls.gryffindor, cls.hufflepuff, cls.ravenclaw, cls.slytherin:
            x, y = house.position, house.grades[course]
            axs.bar(x, y, color=house.color, width=1)

    @classmethod
    def make_scatter_plot(cls, axs, course_x, course_y):
        for house in cls.gryffindor, cls.hufflepuff, cls.ravenclaw, cls.slytherin:
            x, y = house.raw_grades[course_x], house.raw_grades[course_y]
            axs.scatter(x, y, s=1, c=house.color)

    @classmethod
    def set_labels(cls, fig, axs):
        """Set label for each Hogwarts house and each course

        Keyword arguments:
        fig -- object to manipulate figure general appearence
        axs -- object to manipulate x, y axes
        """
        fig.legend([cls.gryffindor.name, cls.hufflepuff.name,
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
    plt.subplots_adjust(top=1, bottom=0.15,
                        right=1, left=0.15,
                        hspace=0, wspace=0)
    plt.show()

if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        print("Example usage: ./pair_plot.py dataset_train.csv")
    except (FileNotFoundError, StopIteration):
        print(f"Dataset file '{sys.argv[1]}' doesn't exist, is empty or incorrect")
    except (IndexError, ValueError):
        print("Check that your dataset has all info about the student (6 first columns),\n"
              "at least two courses (starting from 7th column)\n"
              "and at least one student (row)")