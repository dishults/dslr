#!/usr/bin/env python3
import sys, csv
import numpy as np
import sklearn.metrics as check

from describe import Data, Students, Features
from logreg_predict import Predict

class LogisticRegression:
    
    def __init__(self, learning_rate=0.1, max_interations=200):
        self.alpha = learning_rate
        self.interations = max_interations
        
    def gradient_descent(self, X, theta, y, m):
        """Update theta values through vectorized implementation of GD"""

        z = X.dot(theta)
        h = Predict.g(z)
        gradient = np.dot(X.T, (h - y)) / m
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
            self.theta.append((theta, house))

    def predict(self, X):
        X = np.insert(X, 0, 1, axis=1)
        Y = []
        for x in X:
            probability_of_y = []
            for theta, y in self.theta:
                h = Predict.h(x, theta)
                probability_of_y.append((h, y))
            h, y = max(probability_of_y)
            Y.append(y)
        return Y

    @staticmethod
    def find_perfect_fit():
        combo = {}

        courses_nb = len(Courses.courses)
        c = 0
        c1 = 0
        grades, Y_original = Courses.grades_normalized, Courses.Y
        while c1 < courses_nb:
            c2 = c1 + 1
            while  c2 < courses_nb:
                c3 = c2 + 1
                while c3 < courses_nb:
                    c4 = c3 + 1
                    while c4 < courses_nb:
                        c5 = c4 + 1
                        while c5 < courses_nb:
                            X = [[x[c1], x[c2], x[c3], x[c4], x[c5]] for x in grades]
                            model = LogisticRegression()
                            model.fit(X, Y_original)
                            Y_predicted = model.predict(X)
                            accuracy = check.accuracy_score(Y_original, Y_predicted)
                            combo[c] = {
                                "combo" : [c1, c2, c3, c4, c5],
                                "accuracy" : accuracy
                            }
                            print(c1, c2, c3, c4, c5, "\t", "." * int(accuracy * 100), accuracy)
                            c += 1
                            c5 += 1
                        c4 += 1
                    c3 += 1
                c2 += 1
            c1 += 1
        found = combo[0]
        for c in range(1, len(combo)):
            if combo[c]["accuracy"]["all"] > found["accuracy"]["all"]:
                found = combo[c]
        return found


class Courses():

    houses = ("Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin")
    courses = []
    grades_normalized = []
    Y = []
    m = 0

    def __init__(self, course):
        self.name = course
        self.index = Features.titles.index(course)
        self.avg = Data.info[self.index]["Mean"]
        self.range = Data.info[self.index]["Max"] - Data.info[self.index]["Min"]
        Courses.courses.append(self)

    @staticmethod
    def get_courses(courses):
        for course in courses:
            Courses(course)

    @classmethod
    def get_normalized_grades(cls):
        """Normalize through Feature Scaling (dividing by "max-min")
        and Mean Normalization (substracting average).
        """

        for grades in Students.students:
            normalized = []
            for course in cls.courses:
                try:
                    normalized.append((grades[course.index] - course.avg) / course.range)
                except:
                    normalized.append(0)

            cls.grades_normalized.append(normalized)
            cls.Y.append(cls.houses.index(grades[1]))
            cls.m += 1

   
def main():

    assert len(sys.argv) == 2

    Data(sys.argv[1])
    if Students.nb == 0: raise ValueError
    Features.analyze()

    courses = ("Herbology", "Defense Against the Dark Arts",
                "Divination", "Ancient Runes", "Transfiguration")

    #courses = Features.titles[6:]
    
    Courses.get_courses(courses)
    Courses.get_normalized_grades()
    model = LogisticRegression()

    X, Y_original = Courses.grades_normalized, Courses.Y
    model.fit(X, Y_original)
    Y_predicted = model.predict(X)
    accuracy = check.accuracy_score(Y_original, Y_predicted)
    print(f"Finished training. Precision of algorithm is {accuracy * 100} %")

    #found = model.find_perfect_fit()
    #c = found["combo"]
    #print(found, f"\nCourses:\n-{courses[c[0]]}\n-{courses[c[0]]}\n-{courses[c[0]]}\n-{courses[c[0]]}\n-{courses[c[0]]}")

    with open("weights.csv", 'w') as res:
        writer = csv.writer(res)
        for theta in model.theta:
            writer.writerow(theta[0])
        for i in range(len(Courses.courses)):
            writer.writerow([Courses.courses[i].avg, Courses.courses[i].range])


if __name__ == "__main__":
    main()
