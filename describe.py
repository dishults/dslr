#!/usr/bin/env python3

'''
Takes a dataset as a parameter and 
displays information for all numerical features
'''

import csv, sys, os

from calculations import *

PADDING = 4

class Data:

    header = []
    features_nb = 0
    width = []
    total_width = 0
    students = []
    students_nb = 0
    info = []

    def __init__(self, dataset):
        with open(dataset) as file:
            data = csv.reader(file)
            self.header = next(data)
            self.features_nb = len_(self.header)
            self.width = [len(word) + PADDING for word in self.header]
            for student in data:
                self.transform_numbers(student)
                self.students.append(student)
                self.students_nb += 1        

    def __str__(self, columns=80, lines=24):
        try:
            columns, lines = os.get_terminal_size()
        except:
            pass
        i = 0
        while i < self.features_nb:
            self.print_header(columns, i)
            i = self.print_calculations(columns, i)
            if i < self.features_nb:
                print("\n")             
        return ''
    
    def print_header(self, terminal_width, i):
        printed = 5 #length of the word "Count"
        print(f"{'':<{printed}}", end="")
        while i < self.features_nb and printed + self.width[i] <= terminal_width:
            print(f"{self.header[i]:>{self.width[i]}}", end="")
            printed += self.width[i]
            i += 1
    
    def print_calculations(self, terminal_width, start):
        for key in ("Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"):
            printed = 5
            print(f"\n{key:<{printed}}", end="")
            i = start
            while i < self.features_nb and printed + self.width[i] <= terminal_width:
                if key == "Count" and "Max" not in self.info[i]:
                    print(f"{self.info[i][key]:>{self.width[i]}}", end="")
                elif key in self.info[i]:
                    print(f"{self.info[i][key]:>{self.width[i]}.6f}", end="")
                else:
                    print(f"{'NaN':>{self.width[i]}}", end="")
                printed += self.width[i]
                i += 1
        return i

    def transform_numbers(self, student):
        for i in range(len(student)):
            try:
                student[i] = float(student[i])
            except:
                pass

    def analyze_features(self):
        for f in range(self.features_nb):
            feature = [self.students[s][f] for s in range(self.students_nb)]
            self.make_calculations(feature)
        
        for f in range(self.features_nb):
            self.width[f] = max_([self.width[f], self.info[f]["width"]])
        self.total_width = sum_(self.width) + 5
    
    def make_calculations(self, data):
        info = {}
        info["Count"] = count_(data)
        data = remove_empty_strings(data)
        if count_(data, 'numbers') == info["Count"]:
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

if __name__ == "__main__":
    try:
        assert len(sys.argv) == 2
        DATA = Data(sys.argv[1])
        DATA.analyze_features()
        print(DATA)

        #print("\n")
        #from print_pandas_info import print_padas_info as ppi #tmp
        #ppi(sys.argv[1]) #tmp
    except AssertionError:
        print("Example usage: ./describe.py dataset_train.csv")
        