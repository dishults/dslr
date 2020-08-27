import matplotlib.pyplot as plt

from describe import Data, Students, Features
from DSCRB.calculations import mean_

class Hogwarts:

    houses = []

    def __init__(self, name, color, position):
        self.name = name
        self.color = color
        self.position=position
        if not self.houses:
            self.houses = Students.get_one_feature(1)

    def get_grades(self, course):
        course_nb = Features.titles.index(course)
        grades = Students.get_one_feature(course_nb)
        grades = [grade if grade != '' else 0 for grade in grades]
        return [grades[i] for i in range(len(grades)) if self.houses[i] == self.name]

    @staticmethod
    def normalize_grades(course, max_range=100):
        i = Features.titles.index(course)
        try:
            max_grade = Data.info[i]["Max"]
            min_grade = Data.info[i]["Min"]
        except:
            return

        for house in Gryffindor.grades, Hufflepuff.grades, \
                        Ravenclaw.grades, Slytherin.grades:
            try:
                if max_grade > 0:
                    house[course] = (house[course] * max_range) // max_grade
                elif max_grade < 0:
                    house[course] = (house[course] * -max_range) // min_grade 
            except:
                pass

    def plot(self, course, score, label=None):
        plt.bar(course + self.position, score, color=self.color, width=1, label=label)


class Gryffindor(Hogwarts):

    grades = {}

    def __init__(self):
        super().__init__("Gryffindor", 'maroon', 1)
    
    def get_grades(self, course):
        grades = super().get_grades(course)
        self.grades[course] = mean_(grades)
    
    def set_label(self, course):
        super().plot(0, self.grades[course], label=self.name)


class Hufflepuff(Hogwarts):
    
    grades = {}

    def __init__(self):
        super().__init__("Hufflepuff", 'orange', 2)

    def get_grades(self, course):
        grades = super().get_grades(course)
        self.grades[course] = mean_(grades)

    def set_label(self, course):
        super().plot(0, self.grades[course], label=self.name)


class Ravenclaw(Hogwarts):
    
    grades = {}
    
    def __init__(self):
        super().__init__("Ravenclaw", 'blue', 3)

    def get_grades(self, course):
        grades = super().get_grades(course)
        self.grades[course] = mean_(grades)

    def set_label(self, course):
        super().plot(0, self.grades[course], label=self.name)


class Slytherin(Hogwarts):
    
    grades = {}
    
    def __init__(self):
        super().__init__("Slytherin", 'green', 4)

    def get_grades(self, course):
        grades = super().get_grades(course)
        self.grades[course] = mean_(grades)

    def set_label(self, course):
        super().plot(0, self.grades[course], label=self.name)
