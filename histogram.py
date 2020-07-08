#!/usr/bin/env python3
"""
Script which displays a histogram answering the next question:
Which Hogwarts course has a homogeneous score distribution
between all four houses?
"""

import sys
import matplotlib.pyplot as plt

from describe import Data, Students, Features
from calculations import *

class Hogwarts:

    houses = []

    def __init__(self, color, position):
        self.color = color
        self.position=position
        self.houses = Students.get_one_feature(1)

    def get_grades(self, house, course):
        course_nb = Features.titles.index(course)
        grades = Students.get_one_feature(course_nb)
        grades = [grade for grade in grades if grade != '']
        return [grades[i] for i in range(len(grades)) if self.houses[i] == house]

    @staticmethod
    def get_normalized_mean(grades):
        max_height = 100

        if not grades:
            return 0
        elif len(grades) == 1:
            while (grades[0] > max_height):
                grades[0] = grades[0] // 10
            return grades[0]

        return abs((max_height * mean_(grades)) // max_(grades))

    def plot(self, course, score):
        plt.bar(course + self.position, score, color=self.color, width=1)

class Gryffindor(Hogwarts):

    grades = {}

    def __init__(self):
        super().__init__('maroon', 1)
    
    def get_grades(self, course):
        grades = super().get_grades("Gryffindor", course)
        self.grades[course] = super().get_normalized_mean(grades)

class Hufflepuff(Hogwarts):
    
    grades = {}

    def __init__(self):
        super().__init__('orange', 2)

    def get_grades(self, course):
        grades = super().get_grades("Hufflepuff", course)
        self.grades[course] = super().get_normalized_mean(grades)

class Ravenclaw(Hogwarts):
    
    grades = {}
    
    def __init__(self):
        super().__init__('blue', 3)

    def get_grades(self, course):
        grades = super().get_grades("Ravenclaw", course)
        self.grades[course] = super().get_normalized_mean(grades)

class Slytherin(Hogwarts):
    
    grades = {}
    
    def __init__(self):
        super().__init__('green', 4)

    def get_grades(self, course):
        grades = super().get_grades("Slytherin", course)
        self.grades[course] = super().get_normalized_mean(grades)

def plot():
    g = Gryffindor()
    h = Hufflepuff()
    r = Ravenclaw()
    s = Slytherin()

    courses = Features.titles[6:]

    for course in courses:
        g.get_grades(course)
        h.get_grades(course)
        r.get_grades(course)
        s.get_grades(course)

    plt.xlabel('Courses')
    plt.ylabel('Scores')
    position = 0
    for course in courses:
        g.plot(position, g.grades[course])
        h.plot(position, h.grades[course])
        r.plot(position, r.grades[course])
        s.plot(position, s.grades[course])
        plt.bar(position + 5, 0, width=0)
        position += 5
    plt.show()

def main():
    try:
        assert len(sys.argv) == 2
        data = Data(sys.argv[1])
        plot()

    except AssertionError:
        print("Example usage: ./histogram.py dataset_train.csv")
        

if __name__ == "__main__":
    main()