#!/usr/bin/env python3
"""
Script which displays a histogram answering the next question:
Which Hogwarts course has a homogeneous score distribution
between all four houses?
"""

import sys
import matplotlib.pyplot as plt

from describe import Data, Students, Features
from hogwarts import Hogwarts, Gryffindor, Hufflepuff, Ravenclaw, Slytherin
from calculations import max_, min_, count_, remove_empty_strings

class HistogramFeatures(Features):

    @classmethod
    def analyze(cls):
        for f in range(cls.nb):
            feature = Students.get_one_feature(f)
            cls.make_calculations(feature)
    
    @staticmethod
    def make_calculations(data):
        info = {"Count" : count_(data)}
        data = remove_empty_strings(data)
        if info["Count"] > 0 and count_(data, "numbers") == info["Count"]:
            info["Max"] = max_(data)
            info["Min"] = min_(data)
        Data.info.append(info)


def get_grades(courses, gryffindor, hufflepuff, ravenclaw, slytherin):
    for course in courses:
        for house in gryffindor, hufflepuff, ravenclaw, slytherin:
            house.get_grades(course)
    
    HistogramFeatures.analyze()
    for course in courses:
        Hogwarts.normalize_grades(course)    

def plot(courses, gryffindor, hufflepuff, ravenclaw, slytherin):
    for house in gryffindor, hufflepuff, ravenclaw, slytherin:
        house.set_label(courses[0])
    position = 5
    
    for course in courses[1:]:
        for house in gryffindor, hufflepuff, ravenclaw, slytherin:
            house.plot(position, house.grades[course])
        position += 5
        plt.bar(position, 0, width=0)

def make_histogram(courses):
    fig = plt.figure(figsize=(18, 7))
    fig.suptitle("Courses")
    plt.ylabel("Scores range", fontsize='large')
    yield
    plt.yticks([])
    plt.xticks(list(range(4, len(courses) * 5, 5)), courses)
    fig.autofmt_xdate()
    plt.legend()
    plt.show()
    yield

def main():
    assert len(sys.argv) == 2

    Data(sys.argv[1])
    if Students.nb == 0: raise ValueError

    gryffindor, hufflepuff, ravenclaw, slytherin = \
        Gryffindor(), Hufflepuff(), Ravenclaw(), Slytherin()

    courses = Features.titles[6:]
    histogram = make_histogram(courses)
    next(histogram)

    get_grades(courses, gryffindor, hufflepuff, ravenclaw, slytherin)
    plot(courses, gryffindor, hufflepuff, ravenclaw, slytherin)
    next(histogram)


if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        print("Example usage: ./histogram.py dataset_train.csv")
    except (FileNotFoundError, StopIteration):
        print(f"Dataset file '{sys.argv[1]}' doesn't exist, is empty or incorrect")
    except (IndexError, ValueError):
        print("Check that your dataset has all info about the student (6 first columns),\n"
              "at least one course (starting from 7th column)\n"
              "and at least one student (row)")
