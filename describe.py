#!/usr/bin/env python3

'''
Takes a dataset as a parameter and 
displays information for all numerical features
'''

import csv
import sys
import shutil

from calc import *

PADDING = 4

class Data:

    header = []
    features_number = 0
    width = []
    total_width = 0
    students = []
    students_number = 0
    info = []

    def __init__(self, dataset):
        with open(dataset) as file:
            data = csv.reader(file)
            self.header = next(data)
            self.features_number = len_(self.header)
            self.width = [len(word) + PADDING for word in self.header]
            for student in data:
                self.transform_numbers(student)
                self.students.append(student)
                self.students_number += 1        

    def __str__(self):
        terminal_width, height = shutil.get_terminal_size()
        i = 0
        while i < self.features_number:
            self.print_header(terminal_width, i)
            i = self.print_calculations(terminal_width, i)
            if i < self.features_number:
                print("\n")             
        return ''
    
    def print_header(self, terminal_width, i):
        printed = 5 #length of the word "Count"
        print(f"{'':<{printed}}", end="")
        while i < self.features_number and printed + self.width[i] <= terminal_width:
            print(f"{self.header[i]:>{self.width[i]}}", end="")
            printed += self.width[i]
            i += 1
    
    def print_calculations(self, terminal_width, ii):
        for key in ("Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"):
            printed = 5
            print(f"\n{key:<{printed}}", end="")
            i = ii
            while i < self.features_number and printed + self.width[i] <= terminal_width:
                if "Max" in self.info[i] or key == "Count":
                    print(f"{self.info[i][key]:>{self.width[i]}.6f}", end="")
                else:
                    print(f"{'NaN':>{self.width[i]}}", end="")
                printed += self.width[i]
                i += 1
        return i

    def transform_numbers(self, student):
        for i in range(len(student)):
            if student[i].isdigit():
                student[i] = int(student[i])

    def analyze_features(self):
        [self.make_calculations([self.students[i][x] for i in range(self.students_number)]) for x in range(self.features_number)]
        for i in range(len_(self.width)):
            self.width[i] = max_([self.width[i], self.info[i]["width"]])
        self.total_width = sum_(self.width) + 5
    
    def make_calculations(self, data):
        info = {}
        info["Count"] = count_(data)
        if all_nums(data):
            info["Mean"] = mean_(data)
            info["Std"] = std_(data, info["Mean"])
            info["Min"] = min_(data)
            info["25%"] = percentile_(data, 25)
            info["50%"] = percentile_(data, 50)
            info["75%"] = percentile_(data, 75)
            info["Max"] = max_(data)
        info["width"] = max_([len_(num) for num in info.values()]) + 7 + PADDING
        self.info.append(info)

if __name__ == "__main__":
    try:
        assert len(sys.argv) == 2
        DATA = Data(sys.argv[1])
        DATA.analyze_features()
        print(DATA)

        #from print_pandas_info import print_padas_info as ppi #tmp
        #ppi(sys.argv[1]) #tmp
    except AssertionError:
        print("Example usage: ./describe.py dataset_train.csv")
        