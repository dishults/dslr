#!/usr/bin/env python3
"""
Take a dataset as a parameter and 
display information for all numerical features
"""

import csv, sys, os

from calculations import *
from d_print import Print

PADDING = 4

class Data:

    features = []
    features_nb = 0
    width = []
    total_width = 0
    info = []

    def __init__(self, dataset):
        with open(dataset) as file:
            data = csv.reader(file)
            self.features = next(data)
            self.features_nb = len_(self.features)
            self.width = [len_(word) + PADDING for word in self.features]
            for student in data:
                Students(student)

    def __str__(self, columns=80, lines=24):
        try:
            columns, lines = os.get_terminal_size()
        except:
            pass
        i = 0
        while i < self.features_nb:
            Print.features(self, columns, i)
            i = Print.calculations(self, columns, i)
            if i < self.features_nb:
                print("\n")             
        return ''

    def analyze_features(self):
        for f in range(self.features_nb):
            feature = Students.get_one_feature(f)
            self.make_calculations(feature)
    
    def make_calculations(self, data):
        info = {}
        info["Count"] = count_(data)
        data = remove_empty_strings(data)
        if info["Count"] > 0 and count_(data, 'numbers') == info["Count"]:
            sort_(data)
            info["Mean"] = mean_(data)
            info["Std"] = std_(data, info["Mean"])
            info["Min"] = min_(data)
            info["25%"] = percentile_(data, 25)
            info["50%"] = percentile_(data, 50)
            info["75%"] = percentile_(data, 75)
            info["Max"] = max_(data)
        info["width"] = max_([len_(num) for num in info.values()]) + 7 + PADDING
        self.info.append(info)
    
    def update_width(self):
        for f in range(self.features_nb):
            self.width[f] = max_([self.width[f], self.info[f]["width"]])
        self.total_width = sum_(self.width) + 5

class Students:

    students = []
    students_nb = 0

    @classmethod
    def __init__(cls, student):
        cls.transform(student)
        cls.students.append(student)
        cls.students_nb += 1
    
    @staticmethod
    def transform(student):
        for i in range(len_(student)):
            try:
                student[i] = float(student[i])
            except:
                pass
    
    @classmethod
    def get_one_feature(cls, f):
        return [cls.students[s][f] for s in range(cls.students_nb)]

if __name__ == "__main__":
    try:
        assert len_(sys.argv) == 2
        DATA = Data(sys.argv[1])
        DATA.analyze_features()
        DATA.update_width()
        print(DATA)

    except AssertionError:
        print("Example usage: ./describe.py dataset_train.csv")
        