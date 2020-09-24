#!/usr/bin/env python3
"""
Script which displays a scatter plot answering the next question:
What are the two features that are similar ?
"""

import sys
import matplotlib.pyplot as plt

import my_exceptions as error
from describe import Data, Students, Features
from hogwarts import Hogwarts, Gryffindor, Hufflepuff, Ravenclaw, Slytherin
from DSCRB.calculations import max_, percentile_

class Plot():

    def __init__(self):
        self.courses = Features.titles[6:]
        self.grades = {}

    def get_grades(self):

        def normalize(grade): return int(str(grade).replace('.', '')[:10])

        Students.fix_empty_grades()
        for course in self.courses:
            course_nb = Features.titles.index(course)
            grades = Students.get_one_feature(course_nb)
            grades = [abs(grade) for grade in grades]
            self.grades[course] = [normalize(grade) for grade in grades]

    def find_similar_features(self, fig):
        c = 1
        for course_x in self.courses:
            for course_y in self.courses[c:]:
                grades_x, grades_y = self.grades[course_x], self.grades[course_y]
                diff = set(grades_x) - set(grades_y)
                length = (len(grades_x) + len(grades_y)) // 2
                if (length > 1 and length < 20):
                    five_percent = 1
                else:
                    five_percent = (length * 5) // 100
                if len(diff) <= five_percent:
                    fig.suptitle(f"Two similar features:\n{course_x} - {course_y}")
                    self.course_x = course_x
                    self.course_y = course_y
            c += 1

    def scatter_all_features(self, fig):

        def normalize(grade): return (grade * 100) // max_grade

        for x, course in enumerate(self.courses, 1):
            grades = self.grades[course]
            if (len(grades) >= 100):
                max_grade = max_(grades)
                grades = [percentile_(grades, p) for p in range(1, 100)]
                grades = [normalize(grade) for grade in grades if grade != 0]
            grades = set(grades)
            position = [x] * len(grades)
            plt.scatter(position, list(grades))
        plt.ylabel("Grades", fontsize='large')
        plt.yticks([])
        plt.xticks(list(range(1, len(self.courses) + 1)), self.courses)
        fig.autofmt_xdate()
        plt.show()

    def scatter_similar_features(self):
        houses = Students.get_one_feature(1)
        houses = [house for house in houses if house != 0]
        if len(houses) > 0:
            for house in Gryffindor(), Hufflepuff(), Ravenclaw(), Slytherin():
                house.get_grades(self.course_x)
                house.get_grades(self.course_y)
                house.scatter(self.course_x, self.course_y)
        else:
            x = self.grades[self.course_x]
            y = self.grades[self.course_y]
            x, y = Students.remove_incomplete_grades(courses=[x, y])
            plt.scatter(x, y)
        plt.yticks([]), plt.xticks([])
        plt.xlabel(self.course_x, fontsize='large')
        plt.ylabel(self.course_y, fontsize='large')
        plt.show()


def main():
    if len(sys.argv) != 2: raise error.Usage
    Data(sys.argv[1])

    fig = plt.figure(figsize=(10, 7))

    plot = Plot()
    plot.get_grades()
    plot.find_similar_features(fig)
    plot.scatter_all_features(fig)   
    if 'course_x' in plot.__dict__ and 'course_y' in plot.__dict__:
        plot.scatter_similar_features()
    else:
        print("No similar features found")

if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, StopIteration):
        raise error.File
    except (IndexError, ValueError, KeyError, TypeError):
        raise error.Dataset