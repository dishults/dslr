#!/usr/bin/env python3
"""
Script which displays a scatter plot answering the next question:
What are the two features that are similar ?
"""

import sys
import matplotlib.pyplot as plt

from describe import Data, Students, Features
from calculations import max_, percentile_

class Plot():

    courses = ()
    grades = {}

    @classmethod
    def get_courses(cls):
        cls.courses = Features.titles[6:]

    @classmethod
    def get_grades(cls):
        normalize = lambda grade: int(str(grade).replace('.', '')[:10])
        for course in cls.courses:
            course_nb = Features.titles.index(course)
            grades = Students.get_one_feature(course_nb)
            grades = [abs(grade) if grade != '' else 0 for grade in grades]
            cls.grades[course] = [normalize(grade) for grade in grades]

    @classmethod
    def find_similar_features(cls, fig):
        c = 1
        for course_x in cls.courses:
            for course_y in cls.courses[c:]:
                diff = set(cls.grades[course_x]) - set(cls.grades[course_y])
                length = (len(cls.grades[course_x]) + len(cls.grades[course_y])) // 2
                if (length > 1 and length < 20):
                    five_percent = 1
                else:
                    five_percent = (length * 5) // 100
                if len(diff) <= five_percent:
                    fig.suptitle(f"Two similar features:\n{course_x} - {course_y}")
                    return
            c += 1

    @classmethod
    def scatter(cls):
        x = 1
        normalize = lambda grade: (grade * 100) // max_grade
        for course in cls.courses:
            grades = cls.grades[course]
            if (len(grades) < 100):
                grades = grades
            else:
                max_grade = max_(grades)
                grades = [percentile_(grades, p) for p in range(1, 100)]
                grades = [normalize(grade) for grade in grades if grade != 0]
            grades = set(grades)
            position = [x] * len(grades)
            plt.scatter(position, list(grades))
            x += 1


def main():
    assert len(sys.argv) == 2

    Data(sys.argv[1])
    if Students.nb == 0: raise ValueError

    fig = plt.figure(figsize=(10, 7))

    Plot.get_courses()
    Plot.get_grades()
    Plot.scatter()
    Plot.find_similar_features(fig)

    plt.ylabel("Grades", fontsize='large')
    plt.yticks([])
    plt.xticks(list(range(1, len(Plot.courses) + 1)), Plot.courses)
    fig.autofmt_xdate()
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