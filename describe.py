#!/usr/bin/env python3

'''
Takes a dataset as a parameter and 
displays information for all numerical features
'''

import csv
import sys
from calc import *

class Data:

    header = []
    features_number = 0
    width = []
    students = []
    students_number = 0
    info = []

    def __str__(self):
        return f"\t{self.header}"    

    def get_data(self, dataset):
        with open(dataset) as file:
            data = csv.reader(file)
            self.header = next(data)
            self.features_number = len_(self.header)
            self.width = [len(word) + 4 for word in self.header]
            for student in data:
                self.transform_numbers(student)
                self.students.append(student)
                self.students_number += 1
    
    def transform_numbers(self, student):
        for i in range(len(student)):
            if student[i].isdigit():
                student[i] = int(student[i])
    
    def get_info(self, data):
        info = {}
        info["Count"] = count_(data)
        if all_nums(data):
            info["Mean"] = mean_(data)
            info["Std"] = 0
            info["Min"] = min_(data)
            info["25%"] = percentile_(data, 25)
            info["50%"] = percentile_(data, 50)
            info["75%"] = percentile_(data, 75)
            info["Max"] = max_(data)
        self.info.append(info)

    def print_header(self):
        print(end="\t")
        for i, val in enumerate(self.header):
            print(f"{val:>{self.width[i]}}", end="")
        print()
    
    def print_info(self):        
        for key in ("Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"):
            print(f"{key}", end="\t")
            for i, feature in enumerate(self.info):
                if "Max" not in feature and key != "Count":
                    print(f"{'NaN':>{self.width[i]}}", end="")
                else:
                    print(f"{feature[key]:>{self.width[i]}}", end="")
            print()

if __name__ == "__main__":
    try:
        assert len(sys.argv) == 2
        data = Data()
        data.get_data(sys.argv[1])
        [data.get_info([data.students[i][x] for i in range(data.students_number)]) for x in range(data.features_number)]
        data.print_header()
        data.print_info()
        #from print_pandas_info import print_padas_info as ppi #tmp
        #ppi(sys.argv[1]) #tmp
    except AssertionError:
        print("Example usage: ./describe.py dataset_train.csv")
        