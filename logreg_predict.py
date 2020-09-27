#!/usr/bin/env python3
"""
Sort students into Hogwarts houses
"""

import sys
import csv

import my_exceptions as error
from describe import Data, Students
from DSCRB.calculations import max_
from LOGREG.my_numpy import Numpy as np

HOUSES = ("Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin")

class Predict:

    def __init__(self, weights_csv):
        with open(weights_csv) as weights:
            data = csv.reader(weights)
            if next(data)[0] != "thetas": raise error.Weights
            self.theta = []
            for _ in range(4):
                theta = np.array(next(data)).astype(float)
                self.theta.append(theta)

            if next(data) != ["course index", "average", "range"]: 
                raise error.Weights
            self.courses = []
            for _ in range(5):
                course = next(data)
                self.courses.append({
                    "index" : int(course[0]),
                    "avg"   : float(course[1]),
                    "range" : float(course[2]),
                    })

    @staticmethod
    def h(X, thetas):
        """Hypothesis Function"""

        z = np.dot(thetas.T, X)
        return Predict.g(z)

    @staticmethod
    def g(z):
        """Logistic/Sigmoid Function"""

        return 1 / (1 + np.exp(-z))

    @staticmethod
    def predict(X, all_thetas):
        """Predict Hogwarts houses(Y) for given grades(X)"""

        X = np.insert(X, 0, 1, axis=1)
        Y = []
        for x in X:
            probability_of_y = []
            for y_thetas in all_thetas:
                h = Predict.h(x, y_thetas)
                probability_of_y.append(h)
            y_max = max_(probability_of_y)
            Y.append(probability_of_y.index(y_max))
        return Y

    def get_grades(self):

        def normalize(grade, avg, range_): return (grade - avg) / range_

        self.grades = []
        for student in Students.students:
            grades = []
            for course in self.courses:
                grade = student[course["index"]]
                try:
                    grades.append(
                        normalize(grade, course["avg"], course["range"])
                    )
                except:
                    grades.append(0)
            self.grades.append(grades)


def main():
    if len(sys.argv) != 3: raise error.Usage(stage="test", extra=" weights.csv")
    p = Predict(sys.argv[2])
    Data(sys.argv[1])
    p.get_grades()

    Y_predicted = p.predict(p.grades, p.theta)

    with open("houses.csv", 'w') as res:
        writer = csv.writer(res)
        writer.writerow(["Index", "Hogwarts House"])
        for index, y in enumerate(Y_predicted):
            writer.writerow([index, HOUSES[y]])

if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, StopIteration):
        sys.argv[1] += "' or '" + sys.argv[2]
        raise error.File
    except (IndexError, ValueError, KeyError, TypeError):
        raise error.Dataset