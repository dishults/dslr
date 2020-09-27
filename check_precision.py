#!/usr/bin/env python3

import sklearn.metrics as check
import csv, sys

with open(sys.argv[1]) as one, open(sys.argv[2]) as two:
    file1, file2 = csv.reader(one), csv.reader(two)
    Y1 = [line[1] for line in file1]
    Y2 = [line[1] for line in file2]
    accuracy = check.accuracy_score(Y1, Y2)
    print(f"Precision of algorithm is {accuracy * 100} %")
