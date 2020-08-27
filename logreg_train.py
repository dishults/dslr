#!/usr/bin/env python3
"""
Train through gradient descent multiple sets of parameters theta for 
one-vs-all logistic regression
to sort students into Hogwarts houses
based on grades from best combination of 5 courses
"""

import sys, csv
import numpy as np
import sklearn.metrics as check

from describe import Data, Students, Features
from logreg_predict import Predict, HOUSES

class LogisticRegression:
    
    def __init__(self, learning_rate=0.1, max_interations=200):
        self.alpha = learning_rate
        self.interations = max_interations
        
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
            for _ in range(self.interations):
                theta -= self.gradient_descent(X, theta, y_ova, m)
            self.theta.append(theta) # just theta without house?

    @staticmethod
    def find_perfect_fit():
        """Find the best 5 courses for model training"""

        combo = {}
        courses_nb = len(Courses.courses)
        c = 0
        grades, Y_original = Courses.grades_normalized, Courses.Y
        for c1 in range(courses_nb):
            for c2 in range(c1 + 1, courses_nb):
                for c3 in range(c2 + 1, courses_nb):
                    for c4 in range(c3 + 1, courses_nb):
                        for c5 in range(c4 + 1, courses_nb):
                            X = [[x[c1], x[c2], x[c3], x[c4], x[c5]] for x in grades]
                            model = LogisticRegression(max_interations=150)
                            model.fit(X, Y_original)
                            Y_predicted = Predict.predict(X, model.theta)
                            accuracy = check.accuracy_score(Y_original, Y_predicted)
                            combo[c] = {
                                "combo" : [c1, c2, c3, c4, c5],
                                "accuracy" : accuracy
                            }
                            print(c1, c2, c3, c4, c5, "\t", 
                                    "." * int(accuracy * 100), accuracy)
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
                    normalized.append((grades[course.index] - course.avg) / course.range)
                except:
                    normalized.append(0)

            cls.grades_normalized.append(normalized)
            cls.Y.append(HOUSES.index(grades[1]))
            cls.m += 1


def get_data():
    Data(sys.argv[1])
    if Students.nb == 0: raise ValueError
    Features.analyze()

def get_courses():
    Courses.get_courses()
    Courses.get_normalized_grades()

def bonus_main():
    """Find 5 best courses for model training"""

    assert len(sys.argv) == 3 and sys.argv[2] == "-f"
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
    assert len(sys.argv) == 2
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
        for i in range(len(Courses.analized)):
            course = Courses.analized[i]
            writer.writerow([course.index, course.avg, course.range])

if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        try:
            bonus_main()
        except AssertionError:
            print("Example usage: ./logreg_train.py dataset_train.csv [-f]")
    except (FileNotFoundError, StopIteration):
        print(f"Dataset file '{sys.argv[1]}' doesn't exist, is empty or incorrect")
    except (IndexError, ValueError):
        print("Check that your downloaded dataset is correct and hasn't been altered")