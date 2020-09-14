#!/usr/bin/env python3
"""
Script which displays a pair plot
"""

import sys
import matplotlib.pyplot as plt

import my_exceptions as error

from describe import Data, Students, Features
from histogram import get_grades as get_grades_for_histogram
from hogwarts import Hogwarts, Gryffindor, Hufflepuff, Ravenclaw, Slytherin

class Plot:

    def __init__(self):
        self.courses = Features.titles[6:]
        self.grades = {}

    def get_grades(self):        
        self.gryffindor, self.hufflepuff, self.ravenclaw, self.slytherin = \
            Gryffindor(), Hufflepuff(), Ravenclaw(), Slytherin()

        get_grades_for_histogram(self.courses, 
                                self.gryffindor, self.hufflepuff, 
                                self.ravenclaw, self.slytherin)

        for house in self.gryffindor, self.hufflepuff, self.ravenclaw, self.slytherin:
            house.raw_grades = {}
        for course in self.courses:
            for house in self.gryffindor, self.hufflepuff, self.ravenclaw, self.slytherin:
                house.raw_grades[course] = Hogwarts.get_grades(house, course)

    def pair(self):
        course_nb = len(self.courses)            
        fig, axs = plt.subplots(course_nb, course_nb, figsize=(15, 9))
        row = 0
        for course_y in self.courses:
            col = 0
            for course_x in self.courses:
                if (course_x == course_y):
                    self.make_histogram(axs[row, col], course_x)
                else:
                    self.make_scatter_plot(axs[row, col], course_x, course_y)
                axs[row, col].set_yticks([])
                axs[row, col].set_xticks([])
                col += 1
            row += 1
        self.set_labels(fig, axs)

    def make_histogram(self, axs, course):
        for house in self.gryffindor, self.hufflepuff, self.ravenclaw, self.slytherin:
            x, y = house.position, house.grades[course]
            axs.bar(x, y, color=house.color, width=1)

    def make_scatter_plot(self, axs, course_x, course_y):
        for house in self.gryffindor, self.hufflepuff, self.ravenclaw, self.slytherin:
            x, y = house.raw_grades[course_x], house.raw_grades[course_y]
            axs.scatter(x, y, s=1, c=house.color)

    def set_labels(self, fig, axs):
        """Set label for each Hogwarts house and each course

        Keyword arguments:
        fig -- object to manipulate figure general appearence
        axs -- object to manipulate x, y axes
        """
        fig.legend([self.gryffindor.name, self.hufflepuff.name,
                    self.ravenclaw.name, self.slytherin.name],
                    loc='lower left',
                    borderaxespad=0.1)

        row = 0
        for course in self.courses:
            axs[row, 0].set_ylabel(course, rotation=30, ha='right')
            row += 1

        col = 0
        for course in self.courses:
            axs[-1, col].set_xlabel(course, rotation=30, ha='right')
            col += 1


def main():
    if len(sys.argv) != 2: raise error.Usage
    Data(sys.argv[1], fix_grades=True)

    plot = Plot()
    plot.get_grades()
    plot.pair()
    plt.subplots_adjust(top=1, bottom=0.15,
                        right=1, left=0.15,
                        hspace=0, wspace=0)
    plt.show()

if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, StopIteration):
        raise error.File
    except (IndexError, ValueError):
        raise error.Dataset