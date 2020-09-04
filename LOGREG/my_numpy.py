class Array:

    def __init__(self, data):
        self.data = data
        self.transpose()

    def __str__(self):
        return str(self.data)

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
        """

        C = []
        if type(A) != list:
            A = A.data
        if type(B) != list:
            B = B.data
        # rows of A
        for i in range(len(A)): 
            dot = []
            # coloums of B
            for j in range(len(B[0])): 
                n = 0
                # rows of B
                for k in range(len(B)):
                    n += A[i][k] * B[k][j]
                dot.append(n)
            C.append(dot)
        return Array(C)

    @staticmethod
    def insert(arr, obj, values, axis=None):
        """Insert column of [values] at [obj] position in [arr] and return the copy.
        Variables are preserved for code comparability to numpy,
        though the method handles only axis=1.
        Example:
            np.insert(X, 0, 1, axis=1)
        """

        try:
            dtype = type(arr.data[0][obj])
        except TypeError:
            import sys, traceback
            tb = traceback.format_exc()
            sys.exit(f"{tb}\nCannot insert {values} into array, because it's one-dimensional")
        copy = []
        for X in arr.data:
            duplicate = X[:]
            duplicate.insert(obj, dtype(values))
            copy.append(duplicate)
        return Array(copy)

    @staticmethod
    def zeros(shape):        
        return Array([0] * shape).astype(float)
