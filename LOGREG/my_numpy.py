class Numpy:

    def __init__(self):
        self.array = Array
        self.zeros = self.make_zeros
        self.insert_one = self.make_insert
        self.dot = self.make_dot    

    @staticmethod
    def make_zeros(shape):        
        return Array([0] * shape).astype(float)

    @staticmethod
    def make_insert(X):
        """Same as np.insert(X, 0, 1, axis=1)"""
        try:
            ctype = type(X.data[0])
            copy = []
            for x in X.data:
                copy.append([ctype(1)] + x)
            return Array(copy)
        except:
            return X

    @staticmethod
    def make_dot(A, B):
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
        A = A.data
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

class Array(Numpy):

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.T = self.transpose
        self.astype = self.convert_to_type

    def __str__(self):
        return str(self.data)

    def transpose(self):
        copy = []
        try:
            for j in range(len(self.data[0])):
                new = []
                for i in range(len(self.data)):
                    new.append(self.data[i][j])
                copy.append(new)
        # if only one row
        except:
            for i in range(len(self.data)):
                copy.append([self.data[i]])
        return Array(copy)
    
    def convert_to_type(self, ctype):
        try:
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.data[i][j] = ctype(self.data[i][j])
        # if only one row
        except:
            for i in range(len(self.data)):
                self.data[i] = ctype(self.data[i])
        return self
