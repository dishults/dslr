import matplotlib.pyplot as plt

from describe import Data, Students, Features
from DSCRB.calculations import std_

class Hogwarts:

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.grades = {}
        self.std_diff = {}

    def get_grades(self, course, std_diff=False):
        course_nb = Features.titles.index(course)
        grades = Students.get_one_feature(course_nb, house=self.name)
        self.grades[course] = grades
        if std_diff:
            course_std = Data.info[course_nb]["Std"]
            house_std = std_(grades)
            self.std_diff[course] = (course_std - house_std) * 100 / course_std

    def hist(self, course, axs=None):
        grades = self.grades[course]
        settings = {"x": grades, "facecolor": self.color, "alpha": 0.75}
        try:
            axs.hist(**settings)
        except:
            plt.hist(**settings)

    def scatter(self, course_x, course_y, axs=None):
        x, y = self.grades[course_x], self.grades[course_y]
        x, y = Students.remove_incomplete_grades(courses=[x, y])
        settings = {"x": x, "y": y, "c": self.color}
        try:
            axs.scatter(**settings, s=1)
        except:
            plt.scatter(**settings)


class Gryffindor(Hogwarts):

    def __init__(self):
        super().__init__("Gryffindor", 'maroon')

class Hufflepuff(Hogwarts):
    
    def __init__(self):
        super().__init__("Hufflepuff", 'orange')

class Ravenclaw(Hogwarts):
    
    def __init__(self):
        super().__init__("Ravenclaw", 'blue')

class Slytherin(Hogwarts):
    
    def __init__(self):
        super().__init__("Slytherin", 'green')