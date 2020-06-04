#!/usr/bin/env python3
import unittest
from calculations import *

class test_calculations(unittest.TestCase):
    def test_len(self):
        self.assertEqual(len_(1), 1)
        self.assertEqual(len_(12), 2)
        self.assertEqual(len_(12345435435453435), 17)
        
    def test_percentile(self):
        self.assertEqual(percentile_([1, 2, 3], 50), 2)
        self.assertEqual(percentile_([1, 2, 3, 4], 50), 2.5)

    def test_max(self):
        self.assertEqual(max_([1, 2, 3, 24, 12]), 24)


if __name__ == "__main__":
    unittest.main()