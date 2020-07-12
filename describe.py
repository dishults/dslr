#!/usr/bin/env python3
"""
Take a dataset as a parameter and 
display information for all numerical features
"""

import csv, sys, os

from calculations import *
from d_print import Print, DP, PRINTED

PADDING = 4

class Data:

    info = []

    def __init__(self, dataset):
        with open(dataset) as file:
            data = csv.reader(file)
            Features(next(data))            
            for student in data:
                Students(student)

    def __str__(self, columns=80, lines=24):
        try:
            columns, lines = os.get_terminal_size()
        except:
            pass
        i = 0
        while i < Features.nb:
            Print.features(self, Features, columns, i)
            i = Print.calculations(self, Features, columns, i)
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
        for i in range(len_(student)):
            try:
                student[i] = float(student[i])
            except:
                pass
    
    @classmethod
    def get_one_feature(cls, f):
        return [cls.students[s][f] for s in range(cls.nb)]

class Features:

    titles = []
    nb = 0
    width = []
    total_width = 0

    @classmethod
    def __init__(cls, data):
        cls.titles = data
        cls.nb = len_(cls.titles)
        cls.width = [len_(word) + PADDING for word in cls.titles]

    @classmethod
    def analyze(cls):
        for f in range(cls.nb):
            feature = Students.get_one_feature(f)
            cls.make_calculations(feature)
        cls.update_width()
    
    @staticmethod
    def make_calculations(data):
        info = {"Count" : count_(data)}
        data = remove_empty_strings(data)
        if info["Count"] > 0 and count_(data, "numbers") == info["Count"]:
            sort_(data)
            info["Mean"] = mean_(data)
            info["Std"] = std_(data, info["Mean"])
            info["Min"] = min_(data)
            info["25%"] = percentile_(data, 25)
            info["50%"] = percentile_(data, 50)
            info["75%"] = percentile_(data, 75)
            info["Max"] = max_(data)
        info["width"] = max_([len_(num) for num in info.values()]) + (1+DP) + PADDING
        Data.info.append(info)

    @classmethod
    def update_width(cls):
        for f in range(Features.nb):
            cls.width[f] = max_([cls.width[f], Data.info[f]["width"]])
        cls.total_width = sum_(cls.width) + PRINTED

def main():
    assert len_(sys.argv) == 2
    data = Data(sys.argv[1])
    Features.analyze()
    print(data)

if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        print("Example usage: ./describe.py dataset_train.csv")
    except (FileNotFoundError, StopIteration):
        print(f"Dataset file '{sys.argv[1]}' doesn't exist, is empty or incorrect")