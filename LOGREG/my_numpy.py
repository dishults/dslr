class Array:

    def __init__(self, data):
        self.data = data
        self.len = len(data)

    def __getitem__(self, item):
        return self.data[item]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return self.len

    def __str__(self):
        return str(self.data)

    def math(self, other, f):
        """Peform math operation [f] (+ - * / **) on [self] and [other].

        Keyword arguments:
        other -- int/float or list/Array
        f -- function with operation (+ - * / **) to perform on [self] and [other]
        """

        res = []
        # if both are 1D arrays (self is Array, other is list or Array)
        try:
            assert len(self) == len(other)
            for i in range(len(other)):
                res.append(f(self[i], other[i]))
        except:
            # if self is 2D array and other is int/float
            try:
                for row in self:
                    res.append([f(item, other) for item in row])
            # if self is 1D array and other is int/float
            except:
                for item in self:
                    res.append(f(item, other))
        return Array(res)

    def __add__(self, other):
        return self.math(other, lambda a, b: a + b)

    def __sub__(self, other):
        return self.math(other, lambda a, b: a - b)

    def __mul__(self, other):
        return self.math(other, lambda a, b: a * b)

    def __truediv__(self, other):
        return self.math(other, lambda a, b: a / b)

    def __radd__(self, other):
        return self.math(other, lambda a, b: b + a)

    def __rsub__(self, other):
        return self.math(other, lambda a, b: b - a)

    def __rmul__(self, other):
        return self.math(other, lambda a, b: b * a)

    def __rtruediv__(self, other):
        return self.math(other, lambda a, b: b / a)

    def __rpow__(self, other):
        return self.math(other, lambda a, b: b ** a)

    def __isub__(self, other):
        """self -= other"""
        return self.__sub__(other)

    def __neg__(self):
        """-self"""
        return self.__mul__(-1)

    def astype(self, dtype=float):
        try:
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.data[i][j] = dtype(self.data[i][j])
        # if only one row
        except:
            for i in range(len(self.data)):
                self.data[i] = dtype(self.data[i])
        return self

    def dot(self, other):
        return Numpy.dot(self, other)

    @property
    def T(self):
        try:
            return self._transposed
        except AttributeError:
            self.T = self.data
            return self._transposed

    @T.setter
    def T(self, data):
        self._transposed = []
        try:
            for j in range(len(data[0])):
                new = []
                for i in range(len(data)):
                    new.append(data[i][j])
                self._transposed.append(new)
        # if only one row
        except:
            for i in range(len(data)):
                self._transposed.append([data[i]])


class Numpy:

    array = Array

    @staticmethod
    def dot(A, B):
        """Matrix-Matrix Multiplication.
        From Wikipedia: the entry Cij of the product is obtained by multiplying 
        term-by-term the entries of the ith row of A and the jth column of B, 
        and summing these n products. In other words, Cij is
        the dot product of the ith row of A and the jth column of B.

        Example from Coursera's Machine Learning (Stanford) course:
        [ a b           [ w x           [ a∗w+b∗y a∗x+b∗z
          c d       *     y z ]     =     c∗w+d∗y c∗x+d∗z
          e f ]                           e∗w+f∗y e∗x+f∗z ]

        Keyword arguments:
        A - list or Array with numbers (1 or 2 dimensional)
        B - list or Array with numbers (1 or 2 dimensional)
        """

        C = []
        A_rows, B_rows = len(A), len(B)
        # if both A and B are 2D
        try:
            B_columns = len(B[0])
            for i in range(A_rows):
                dot = []
                for j in range(B_columns):
                    n = 0
                    for k in range(B_rows):
                        n += A[i][k] * B[k][j]
                    dot.append(n)
                C.append(dot)
        except:
            B_columns = B_rows
            # if both A and B are 1D
            if A_rows == B_columns:
                dot = 0
                for i in range(A_rows):
                    dot += A[i][0] * B[i]
                return dot
            # if A is 2D and B is 1D
            else:
                for i in range(A_rows):
                    dot = 0
                    for k in range(B_columns):
                        dot += A[i][k] * B[k]
                    C.append(dot)
        return Array(C)

    @staticmethod
    def exp(x, e=2.718281828459045):
        """Calculate the exponential of x (e raised to the power of x).

        Keyword arguments:
        x -- int/float or Array
        e -- float. The irrational number, also known as Euler’s number
             It's approx 2.718281, and is the base of the natural logarithm
        """

        return e ** x

    @staticmethod
    def insert(arr, obj, values, axis=None):
        """Insert column of [values] at [obj] position in [arr] and return the copy.
        Variables are preserved for code comparability to numpy,
        though the method handles only axis=1.

        Example:
            np.insert(X, 0, 1, axis=1)

        Keyword arguments:
        arr -- Array to insert into
        obj -- position in Array
        values -- int, float or list to insert
        """

        try:
            dtype = type(arr[0][obj])
        except TypeError:
            import sys
            import traceback
            tb = traceback.format_exc()
            sys.exit(
                f"{tb}\nCannot insert {values} into array, because it's one-dimensional")

        copy = []
        for X in arr:
            duplicate = X[:]
            duplicate.insert(obj, dtype(values))
            copy.append(duplicate)
        return Array(copy)

    @staticmethod
    def zeros(shape):
        return Array([0] * shape).astype(float)
