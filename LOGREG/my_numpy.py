class Array:

    def __init__(self, data):
        self.data = data
        self.transpose()
    
    def __iter__(self):
        return iter(self.data)

    def __str__(self):
        return str(self.data)
    
    def __getitem__(self, item):
         return self.data[item]

    def math(self, other, f):
        """Peform math operation [f] (+ - * /) on [self] Array with [other] number.

        Keyword arguments:
        other -- int or float
        f -- function with operation (+ - * /) to perform
        """
        res = []
        try:
            for row in self.data:
                new = []
                for item in row:
                    new.append(f(item, other))
                res.append(new)
        # if only one row
        except:
            for item in self.data:
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

    def astype(self, ctype):
        try:
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.data[i][j] = ctype(self.data[i][j])
        # if only one row
        except:
            for i in range(len(self.data)):
                self.data[i] = ctype(self.data[i])
        self.transpose()
        return self

    def transpose(self):
        self.T = []
        try:
            for j in range(len(self.data[0])):
                new = []
                for i in range(len(self.data)):
                    new.append(self.data[i][j])
                self.T.append(new)
        # if only one row
        except:
            for i in range(len(self.data)):
                self.T.append([self.data[i]])
        
    def dot(self, other):
        return Numpy.dot(self, other)


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
        A - 'Array' object or list with numbers (1 or 2 dimensional)
        B - 'Array' object or list with numbers (1 or 2 dimensional)
        """

        if type(A) != list:
            A = A.data
        if type(B) != list:
            B = B.data
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
        x -- int/float or list.
        e -- float. The irrational number, also known as Euler’s number.
             It's approx 2.718281, and is the base of the natural logarithm.
        """
        try:
            return e ** x
        except:
            try:
                data = x.data
            except:
                data = x
            return Array([e ** nb for nb in data])

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
            array = arr.data
        except AttributeError:
            array = arr
        try:
            dtype = type(array[0][obj])
        except TypeError:
            import sys, traceback
            tb = traceback.format_exc()
            sys.exit(f"{tb}\nCannot insert {values} into array, because it's one-dimensional")

        copy = []
        for X in array:
            duplicate = X[:]
            duplicate.insert(obj, dtype(values))
            copy.append(duplicate)
        return Array(copy)

    @staticmethod
    def zeros(shape):        
        return Array([0] * shape).astype(float)
