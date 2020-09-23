#!/usr/bin/env python3
"""
Train through gradient descent multiple sets of parameters theta for 
one-vs-all logistic regression
to sort students into Hogwarts houses
based on grades from best combination of 5 courses
"""

import sys
import csv
import sklearn.metrics as check

import my_exceptions as error
from describe import Data, Students, Features
from logreg_predict import Predict, HOUSES
from LOGREG.my_numpy import Numpy as np

class LogisticRegression:
    
    def __init__(self, learning_rate=0.1, max_iterations=200):
        self.alpha = learning_rate
        self.iterations = max_iterations
        
    def gradient_descent(self, X, theta, Y, m):
        """Update theta values through vectorized implementation of GD"""

        Z = X.dot(theta)
        H = Predict.g(Z)
        gradient = np.dot(X.T, (H - Y)) / m
        return self.alpha * gradient
    
    def fit(self, X, Y):
        """Calculate optimal thetas to predict future data"""

        def one_vs_all(house): return [1 if y == house else 0 for y in Y]

        self.theta = []
        X = np.insert(X, 0, 1, axis=1)
        m = Courses.m
        theta_nb = len(X[0])

        for house in range(4):
            y_ova = one_vs_all(house)
            theta = np.zeros(theta_nb)
            for _ in range(self.iterations):
                theta -= self.gradient_descent(X, theta, y_ova, m)
            self.theta.append(theta)

    @staticmethod
    def find_perfect_fit():
        """Find the best 5 courses for model training"""

        def run_simultation():
            X = [[x[c1], x[c2], x[c3], x[c4], x[c5]] for x in grades]
            model = LogisticRegression(max_iterations=150)
            model.fit(X, Y_original)

            Y_predicted = Predict.predict(X, model.theta)
            accuracy = check.accuracy_score(Y_original, Y_predicted)
            print(c1, c2, c3, c4, c5, "\t", "." * int(accuracy * 100), accuracy)

            return {
                "combo" : [c1, c2, c3, c4, c5],
                "accuracy" : accuracy,
            }

        combo = {}
        courses_nb = len(Courses.courses)
        c = 0
        grades, Y_original = Courses.grades_normalized, Courses.Y
        for c1 in range(courses_nb):
            for c2 in range(c1 + 1, courses_nb):
                for c3 in range(c2 + 1, courses_nb):
                    for c4 in range(c3 + 1, courses_nb):
                        for c5 in range(c4 + 1, courses_nb):
                            combo[c] = run_simultation()
                            c += 1
        found = combo[0]
        for c in range(1, len(combo)):
            if combo[c]["accuracy"] > found["accuracy"]:
                found = combo[c]
        return found


class Courses():

    courses = ("Herbology", "Defense Against the Dark Arts",
               "Divination", "Ancient Runes", "Flying")
    analized = []
    grades_normalized = []
    Y = []
    m = 0

    def __init__(self, course):
        self.name = course
        self.index = Features.titles.index(course)
        self.avg = Data.info[self.index]["Mean"]
        self.range = Data.info[self.index]["Max"] - Data.info[self.index]["Min"]
        Courses.analized.append(self)

    @classmethod
    def get_courses(cls):
        for course in cls.courses:
            Courses(course)

    @classmethod
    def get_normalized_grades(cls):
        """Normalize through Feature Scaling (dividing by "max-min")
        and Mean Normalization (substracting average).
        """

        for grades in Students.students:
            normalized = []
            for course in cls.analized:
                try:
                    normalized.append(
                        (grades[course.index] - course.avg) / course.range
                    )
                except:
                    normalized.append(0)

            cls.grades_normalized.append(normalized)
            cls.Y.append(HOUSES.index(grades[1]))
            cls.m += 1


def get_data():
    Data(sys.argv[1])
    Features.analyze(depth=0)

def get_courses():
    Courses.get_courses()
    Courses.get_normalized_grades()

def bonus_main():
    """Find 5 best courses for model training"""

    if len(sys.argv) != 3 or sys.argv[2] != "-f": 
        raise error.Usage(extra=" [-f]")
    get_data()
    courses = Features.titles[6:]
    Courses.courses = courses
    get_courses()
    model = LogisticRegression()

    found = model.find_perfect_fit()
    c = found["combo"]
    print(found, f"\nCourses:\n{c[0]} - {courses[c[0]]}",
          f"\n{c[1]} - {courses[c[1]]}\n{c[2]} - {courses[c[2]]}",
          f"\n{c[3]} - {courses[c[3]]}\n{c[4]} - {courses[c[4]]}")

def main():
    if len(sys.argv) != 2: bonus_main()
    get_data()
    get_courses()
    model = LogisticRegression()

    X, Y_original = Courses.grades_normalized, Courses.Y
    model.fit(X, Y_original)
    Y_predicted = Predict.predict(X, model.theta)
    accuracy = check.accuracy_score(Y_original, Y_predicted)
    print(f"Finished training. Precision of algorithm is {accuracy * 100} %")

    with open("weights.csv", 'w') as res:
        writer = csv.writer(res)
        writer.writerow(["thetas"])
        for theta in model.theta:
            writer.writerow(theta)
        writer.writerow(["course index", "average", "range"])
        for course in Courses.analized:
            writer.writerow([course.index, course.avg, course.range])

if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, StopIteration):
        raise error.File
    except (IndexError, ValueError):
        raise error.Dataset