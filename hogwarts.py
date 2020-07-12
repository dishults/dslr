import matplotlib.pyplot as plt

from describe import Data, Students, Features
from calculations import mean_

class Hogwarts:

    houses = []

    def __init__(self, color, position):
        self.color = color
        self.position=position
        if not self.houses:
            self.houses = Students.get_one_feature(1)

    def get_grades(self, house, course):
        course_nb = Features.titles.index(course)
        grades = Students.get_one_feature(course_nb)
        grades = [grade for grade in grades if grade != '']
        return [grades[i] for i in range(len(grades)) if self.houses[i] == house]

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
        super().__init__('maroon', 1)
    
    def get_grades(self, course):
        grades = super().get_grades("Gryffindor", course)
        self.grades[course] = mean_(grades)
    
    def set_label(self, course):
        super().plot(0, self.grades[course], label="Gryffindor")


class Hufflepuff(Hogwarts):
    
    grades = {}

    def __init__(self):
        super().__init__('orange', 2)

    def get_grades(self, course):
        grades = super().get_grades("Hufflepuff", course)
        self.grades[course] = mean_(grades)

    def set_label(self, course):
        super().plot(0, self.grades[course], label="Hufflepuff")


class Ravenclaw(Hogwarts):
    
    grades = {}
    
    def __init__(self):
        super().__init__('blue', 3)

    def get_grades(self, course):
        grades = super().get_grades("Ravenclaw", course)
        self.grades[course] = mean_(grades)

    def set_label(self, course):
        super().plot(0, self.grades[course], label="Ravenclaw")


class Slytherin(Hogwarts):
    
    grades = {}
    
    def __init__(self):
        super().__init__('green', 4)

    def get_grades(self, course):
        grades = super().get_grades("Slytherin", course)
        self.grades[course] = mean_(grades)

    def set_label(self, course):
        super().plot(0, self.grades[course], label="Slytherin")
