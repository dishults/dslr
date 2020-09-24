#!/usr/bin/env python3
"""
Take a dataset as a parameter and 
display information for all numerical features
"""

import csv
import sys
import os

import my_exceptions as error
import DSCRB.print as print_

from DSCRB.calculations import \
num_len, sort_, count_, mean_, std_, min_, percentile_, max_
from DSCRB.print import DP, PRINTED, PADDING

class Data:

    info = []

    def __init__(self, dataset, check_houses=False):
        with open(dataset) as file:
            data = csv.reader(file)
            Features(next(data))            
            for student in data:
                Students(student)
        if (Students.nb == 0 or Features.nb < 7
                or ["Index", "Hogwarts House", "First Name",
                    "Last Name","Birthday","Best Hand"] != Features.titles[:6]): 
            raise ValueError
        if check_houses:
            houses = Students.get_one_feature(1)
            houses = [house for house in houses if house != '']
            if len(houses) == 0:
                raise error.Houses

    def __str__(self, columns=80, lines=24):
        try:
            columns, lines = os.get_terminal_size()
        except:
            pass
        i = 0
        while i < Features.nb:
            print_.features(Features, columns, i)
            i = print_.calculations(self, Features, columns, i)
            if i < Features.nb:
                print("\n")
        return ''


class Students:

    students = []
    nb = 0

    @classmethod
    def __init__(cls, student):
        cls.transform(student)
        cls.students.append(student)
        cls.nb += 1
    
    @staticmethod
    def transform(student):
        for i, grade in enumerate(student):
            try:
                student[i] = float(grade)
            except:
                pass
    
    @classmethod
    def get_one_feature(cls, f, house=None):
        """Get one feature(column) or all grades for one subject
        for a specific Hogwarts house
        """

        students = cls.students
        if not house:
            return [students[s][f] for s in range(cls.nb)]
        return [students[s][f] for s in range(cls.nb) if students[s][1] == house]

    @classmethod
    def fix_empty_grades(cls):
        i = 0
        while i < cls.nb:
            if '' in cls.students[i]:
                empty = cls.students[i].index('')
                cls.students[i][empty] = 0
            else:
                i += 1

    @staticmethod
    def remove_incomplete_grades(courses):
        copy = [course[:] for course in courses]
        i = 0
        grades_nb = len(courses[0])
        while i < grades_nb:
            grades = [course[i] for course in copy]
            if 0 in grades:
                [course.pop(i) for course in copy]
                grades_nb -= 1
            else:
                i += 1
        return copy


class Features:

    titles = []
    nb = 0
    width = []

    @classmethod
    def __init__(cls, data):
        if any(cell.isdigit() for cell in data): raise error.Header
        cls.titles = data
        cls.nb = len(data)
        cls.width = [len(title) + PADDING for title in data]

    @classmethod
    def analyze(cls, depth=2):
        for f in range(cls.nb):
            feature = Students.get_one_feature(f)
            info = {"Count" : count_(feature)}
            feature = [f for f in feature if f != '']
            if info["Count"] > 0 and count_(feature, "numbers") == info["Count"]:
                info = cls.make_calculations(info, feature, depth)
            if depth == 2:
                info["width"] = max_([num_len(num) for num in info.values()])
                info["width"] += 1 + DP + PADDING
            Data.info.append(info)

    @staticmethod
    def make_calculations(info, data, depth):
        info["Min"] = min_(data)
        info["Max"] = max_(data)
        info["Mean"] = mean_(data)
        if depth > 0:
            info["Std"] = std_(data, info["Mean"])
        if depth == 2:            
            sort_(data)
            info["25%"] = percentile_(data, 25)
            info["50%"] = percentile_(data, 50)
            info["75%"] = percentile_(data, 75)
        return info

    @classmethod
    def update_width(cls):
        for f in range(Features.nb):
            cls.width[f] = max_([cls.width[f], Data.info[f]["width"]])


def main():
    if len(sys.argv) != 2: raise error.Usage
    data = Data(sys.argv[1])
    Features.analyze()
    Features.update_width()
    print(data)

if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, StopIteration):
        raise error.File
    except (IndexError, ValueError, TypeError, ZeroDivisionError):
        raise error.Dataset