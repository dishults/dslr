#!/usr/bin/env python3
"""
Script which displays a pair plot
"""

import sys
import matplotlib.pyplot as plt

import my_exceptions as error
from describe import Data, Students, Features
from hogwarts import Hogwarts, Gryffindor, Hufflepuff, Ravenclaw, Slytherin

class Plot:

    def __init__(self):
        self.courses = Features.titles[6:]
        self.grades = {}
        self.gryffindor, self.hufflepuff, self.ravenclaw, self.slytherin = \
            Gryffindor(), Hufflepuff(), Ravenclaw(), Slytherin()

    def get_grades(self):
        Students.fix_empty_grades()
        for course in self.courses:
            for house in (self.gryffindor, self.hufflepuff, 
                          self.ravenclaw, self.slytherin):
                house.get_grades(course)

    def pair(self):
        course_nb = len(self.courses)            
        fig, axs = plt.subplots(course_nb, course_nb, figsize=(15, 9))
        for row, course_y in enumerate(self.courses):
            for col, course_x in enumerate(self.courses):
                if course_x == course_y:
                    self.make_histogram(axs[row, col], course_x)
                else:
                    self.make_scatter_plot(axs[row, col], course_x, course_y)
        self.set_labels(fig, axs)

    def make_histogram(self, axs, course):
        for house in (self.gryffindor, self.hufflepuff, 
                      self.ravenclaw, self.slytherin):
            house.hist(course, axs)
            axs.set_yticks([]), axs.set_xticks([])

    def make_scatter_plot(self, axs, course_x, course_y):
        for house in (self.gryffindor, self.hufflepuff, 
                      self.ravenclaw, self.slytherin):
            house.scatter(course_x, course_y, axs)
            axs.set_yticks([]), axs.set_xticks([])

    def set_labels(self, fig, axs, max_len=16):
        """Set label for each Hogwarts house and each course

        Keyword arguments:
        fig -- object to manipulate figure general appearence
        axs -- object to manipulate x, y axes
        """
        
        def str_split(course): return course[:max_len] + '\n' + course[max_len:]
        
        fig.legend([self.gryffindor.name, self.hufflepuff.name,
                    self.ravenclaw.name, self.slytherin.name],
                    loc='lower left', borderaxespad=0.1)

        row = 0
        for course in self.courses:
            if len(course) > max_len:
                course = str_split(course)
            axs[row, 0].set_ylabel(course, rotation=30, ha='right')
            row += 1

        col = 0
        for course in self.courses:
            if len(course) > max_len:
                course = str_split(course)
            axs[-1, col].set_xlabel(course, rotation=30, ha='right')
            col += 1


def main():
    if len(sys.argv) != 2: raise error.Usage
    Data(sys.argv[1], check_houses=True)

    plot = Plot()
    plot.get_grades()
    plot.pair()
    plt.subplots_adjust(top=1, bottom=0.1, left=0.1, right=1, hspace=0, wspace=0)
    plt.show()

if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, StopIteration):
        raise error.File
    except (IndexError, ValueError, KeyError, TypeError):
        raise error.Dataset