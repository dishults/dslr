import numpy as np

class Predict:

    @staticmethod
    def h(X, theta=[0, 0, 0, 0, 0]):
        """Hypothesis Function"""

        z = np.dot(theta.T, X)
        return Predict.g(z)

    @staticmethod
    def g(z):
        """Logistic/Sigmoid Function"""

        return 1 / (1 + np.exp(-z))
    
    @staticmethod
    def cost(X, Y, theta=[0, 0, 0, 0, 0]):
        """Vectorized implementation of the cost function"""
        h = Predict.g(np.dot(X, theta))
        m = len(X)
        y1 = -Y.T * np.log(h)
        y0 = (1 - Y).T * np.log(1 - h)
        return (y1 - y0) / m
