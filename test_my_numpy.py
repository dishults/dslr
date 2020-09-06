#!/usr/bin/env python3
import unittest, numpy

from LOGREG.my_numpy import Numpy as my_np

class Tests(unittest.TestCase):

    x_array = [[1, 2, 3], [1, 2, 3]]
    y_array = [[7, 8, 9], [7, 8, 9]]

    Xn = numpy.array(x_array)
    Yn = numpy.array(y_array)

    Xmy = my_np.array(x_array)
    Ymy = my_np.array(y_array)

    def test_arrays(self):
        self.assertEqual(self.Xn.tolist(), list(self.Xmy))
        self.assertEqual(self.Yn.tolist(), list(self.Ymy))

    def test_astype(self, dtype=float):
        self.assertEqual(self.Xn.astype(dtype).tolist(), list(self.Xmy.astype(dtype)))

    def test_dot_2D(self):
        original = numpy.dot(self.Xn.T, self.Yn)
        my = my_np.dot(self.Xmy.T, self.Ymy)
        self.assertEqual(original.tolist(), list(my))

    def test_dot_y_1D(self, y=[1, 2]):
        original = numpy.dot(self.Xn.T, y)
        my = my_np.dot(self.Xmy.T, y)
        self.assertEqual(original.tolist(), list(my))

    def test_math(self, nb=3):
        original = [(self.Xn+nb).tolist(), (self.Xn-nb).tolist(), (self.Xn*nb).tolist()]
        my = [list(self.Xmy+nb), list(self.Xmy-nb), list(self.Xmy*nb)]
        self.assertEqual(original, my)

    def test_insert_numpy_array(self):
        original = numpy.insert(self.Xn, 0, 1, axis=1)
        my = my_np.insert(self.Xmy, 0, 1, axis=1)
        self.assertEqual(original.tolist(), list(my))

    def test_insert_list(self, sample=[[1, 2, 3], [1, 2, 3]]):
        original = numpy.insert(sample, 0, 1, axis=1)
        my = my_np.insert(sample, 0, 1, axis=1)
        self.assertEqual(original.tolist(), list(my))

    def test_transpose(self):
        self.assertEqual(self.Xn.T.tolist(), list(self.Xmy.T))
        self.assertEqual(self.Yn.T.tolist(), list(self.Ymy.T))

    def test_zeros(self, nb=5):
        self.assertEqual(numpy.zeros(nb).tolist(), list(my_np.zeros(nb)))


if __name__ == "__main__":
    unittest.main()