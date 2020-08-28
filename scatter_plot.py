#!/usr/bin/env python3
"""
Script which displays a scatter plot answering the next question:
What are the two features that are similar ?
"""

import sys
import matplotlib.pyplot as plt

from describe import Data, Students, Features
from DSCRB.calculations import max_, percentile_
from hogwarts import Hogwarts, Gryffindor, Hufflepuff, Ravenclaw, Slytherin

class Plot():

    def __init__(self):
        self.courses = Features.titles[6:]
        self.grades = {}

    def get_grades(self):

        def normalize(grade): return int(str(grade).replace('.', '')[:10])

        for course in self.courses:
            course_nb = Features.titles.index(course)
            grades = Students.get_one_feature(course_nb)
            grades = [abs(grade) if grade != '' else 0 for grade in grades]
            self.grades[course] = [normalize(grade) for grade in grades]

    def find_similar_features(self, fig):
        c = 1
        for course_x in self.courses:
            for course_y in self.courses[c:]:
                diff = set(self.grades[course_x]) - set(self.grades[course_y])
                length = (len(self.grades[course_x]) + len(self.grades[course_y])) // 2
                if (length > 1 and length < 20):
                    five_percent = 1
                else:
                    five_percent = (length * 5) // 100
                if len(diff) <= five_percent:
                    fig.suptitle(f"Two similar features:\n{course_x} - {course_y}")
                    self.course_x = course_x
                    self.course_y = course_y
            c += 1

    def scatter_all_features(self):

        def normalize(grade): return (grade * 100) // max_grade

        x = 1
        for course in self.courses:
            grades = self.grades[course]
            if (len(grades) >= 100):
                max_grade = max_(grades)
                grades = [percentile_(grades, p) for p in range(1, 100)]
                grades = [normalize(grade) for grade in grades if grade != 0]
            grades = set(grades)
            position = [x] * len(grades)
            plt.scatter(position, list(grades))
            x += 1
        plt.ylabel("Grades", fontsize='large')
        plt.yticks([])
        plt.xticks(list(range(1, len(self.courses) + 1)), self.courses)
        
    def scatter_similar_features(self):
        for house in Gryffindor(), Hufflepuff(), Ravenclaw(), Slytherin():
            x = Hogwarts.get_grades(house, self.course_x)
            y = Hogwarts.get_grades(house, self.course_y)
            plt.scatter(x, y, c=house.color)
            plt.xlabel(self.course_x, fontsize='large')
            plt.ylabel(self.course_y, fontsize='large')

def main():
    assert len(sys.argv) == 2

    Data(sys.argv[1])
    if Students.nb == 0: raise ValueError

    fig = plt.figure(figsize=(10, 7))

    plot = Plot()
    plot.get_grades()
    plot.find_similar_features(fig)

    plot.scatter_all_features()
    fig.autofmt_xdate()
    plt.show()

    if plot.course_x and plot.course_y:
        plot.scatter_similar_features()
        plt.show()

if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        print("Example usage: ./scatter_plot.py dataset_train.csv")
    except (FileNotFoundError, StopIteration):
        print(f"Dataset file '{sys.argv[1]}' doesn't exist, is empty or incorrect")
    except (IndexError, ValueError):
        print("Check that your dataset has all info about the student (6 first columns),\n"
              "at least two courses (starting from 7th column)\n"
              "and at least one student (row)")