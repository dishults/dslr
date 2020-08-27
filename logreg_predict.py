#!/usr/bin/env python3
"""
Sort students into Hogwarts houses
"""

import sys, csv
import numpy as np

from describe import Data, Students
from DSCRB.calculations import max_

HOUSES = ("Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin")

class Predict:

    def __init__(self, weights_csv):
        with open(weights_csv) as file:
            data = csv.reader(file)
            if next(data)[0] != "thetas": raise FileExistsError
            self.theta = []
            for _ in range(4):
                theta = np.array(next(data)).astype(float)
                self.theta.append(theta)

            if next(data)[0] != "course index": raise FileExistsError
            self.courses = []
            for _ in range(5):
                course = next(data)
                self.courses.append(
                    {"index" : int(course[0]),
                     "avg"   : float(course[1]),
                     "range" : float(course[2])})

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
    def predict(X, theta=[0, 0, 0, 0, 0]):
        """Predict Hogwarts houses(Y) for given grades(X)"""

        X = np.insert(X, 0, 1, axis=1)
        Y = []
        for x in X:
            probability_of_y = []
            for t in theta:
                h = Predict.h(x, t)
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
                    grades.append(normalize(grade, course["avg"], course["range"]))
                except:
                    grades.append(0)
            self.grades.append(grades)


def main():
    assert len(sys.argv) == 3
    p = Predict(sys.argv[2])
    Data(sys.argv[1])
    p.get_grades()

    Y_predicted = p.predict(p.grades, p.theta)

    with open("houses.csv", 'w') as res:
        writer = csv.writer(res)
        for index, y in enumerate(Y_predicted):
            writer.writerow([index, HOUSES[y]])

if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        print("Example usage: ./logreg_predict.py dataset_test.csv weights.csv.")
    except (FileNotFoundError, StopIteration):
        print(f"Dataset file '{sys.argv[1]}' or '{sys.argv[2]}' doesn't exist, is empty or incorrect.")
    except (FileExistsError):
        print(f"Something went wrong with your '{sys.argv[2]}' file. Double check it's correct.")
    except (IndexError, ValueError):
        print("Check that your downloaded dataset is correct and hasn't been altered.")