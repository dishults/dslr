#!/usr/bin/env python3
import unittest
import pandas as pd
import os

from describe import Data
from d_print import DP

DP -= 1

class Tests(unittest.TestCase):

    #dataset = "datasets/small_set.csv"
    dataset = "datasets/dataset_train.csv"
    #dataset = "datasets/dataset_test.csv"

    my = Data(dataset)
    p_data = pd.read_csv(dataset)

    my.analyze_features()
    p = {
        "Count" : p_data.count(),
        "Mean" : p_data.mean(numeric_only=True),
        "Std" : p_data.std(numeric_only=True),
        "Min" : p_data.min(numeric_only=True),
        "25%" : p_data.quantile(0.25),
        "50%" : p_data.quantile(),
        "75%" : p_data.quantile(0.75),
        "Max" : p_data.max(numeric_only=True)
    }

    def test_describe(self):
        os.system("./describe.py datasets/small_set.csv > test1.txt")
        self.assertFalse(os.system("diff test0.txt test1.txt"))
        os.system("rm -rf test1.txt")

    def test_count(self, key="Count"):
        for i in range(len(self.my.info)):
            self.assertEqual(self.my.info[i][key], self.p[key][i])

    def test_mean(self, key="Mean"):
        j = 0
        for i in range(len(self.my.info)):
            if key in self.my.info[i]:
                self.assertEqual(f"{self.my.info[i][key]:>{0}.{DP}f}",
                                 f"{self.p[key][j]:>{0}.{DP}f}")
                j += 1

    def test_std(self, key="Std"):
        j = 0
        for i in range(len(self.my.info)):
            if key in self.my.info[i]:
                self.assertEqual(f"{self.my.info[i][key]:>{0}.{DP}f}",
                                 f"{self.p[key][j]:>{0}.{DP}f}")
                j += 1

    def test_min(self, key="Min"):
        j = 0
        for i in range(len(self.my.info)):
            if key in self.my.info[i]:
                self.assertEqual(f"{self.my.info[i][key]:>{0}.{DP}f}",
                                 f"{self.p[key][j]:>{0}.{DP}f}")
                j += 1

    def test_25_percentile(self, key="25%"):
        j = 0
        for i in range(len(self.my.info)):
            if key in self.my.info[i]:
                self.assertEqual(f"{self.my.info[i][key]:>{0}.{DP}f}",
                                 f"{self.p[key][j]:>{0}.{DP}f}")
                j += 1

    def test_50_percentile(self, key="50%"):
        j = 0
        for i in range(len(self.my.info)):
            if key in self.my.info[i]:
                self.assertEqual(f"{self.my.info[i][key]:>{0}.{DP}f}",
                                 f"{self.p[key][j]:>{0}.{DP}f}")
                j += 1

    def test_75_percentile(self, key="75%"):
        j = 0
        for i in range(len(self.my.info)):
            if key in self.my.info[i]:
                self.assertEqual(f"{self.my.info[i][key]:>{0}.{DP}f}",
                                 f"{self.p[key][j]:>{0}.{DP}f}")
                j += 1

    def test_max(self, key="Max"):
        j = 0
        for i in range(len(self.my.info)):
            if key in self.my.info[i]:
                self.assertEqual(f"{self.my.info[i][key]:>{0}.{DP}f}",
                                 f"{self.p[key][j]:>{0}.{DP}f}")
                j += 1

if __name__ == "__main__":
    unittest.main()