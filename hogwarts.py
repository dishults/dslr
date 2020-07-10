import matplotlib.pyplot as plt

from describe import Students, Features
from calculations import mean_, max_

class Hogwarts:

    houses = []

    def __init__(self, color, position):
        self.color = color
        self.position=position
        self.houses = Students.get_one_feature(1)

    def get_grades(self, house, course):
        course_nb = Features.titles.index(course)
        grades = Students.get_one_feature(course_nb)
        grades = [grade for grade in grades if grade != '']
        return [grades[i] for i in range(len(grades)) if self.houses[i] == house]

    @staticmethod
    def get_normalized_mean(grades):
        max_height = 100

        if not grades:
            return 0
        elif len(grades) == 1:
            while (grades[0] > max_height):
                grades[0] = grades[0] // 10
            return grades[0]

        return (max_height * mean_(grades)) // max_(grades)

    def plot(self, course, score, label=None):
        plt.bar(course + self.position, score, color=self.color, width=1, label=label)


class Gryffindor(Hogwarts):

    grades = {}

    def __init__(self):
        super().__init__('maroon', 1)
    
    def get_grades(self, course):
        grades = super().get_grades("Gryffindor", course)
        self.grades[course] = super().get_normalized_mean(grades)
    
    def set_label(self, course):
        super().plot(0, self.grades[course], label="Gryffindor")


class Hufflepuff(Hogwarts):
    
    grades = {}

    def __init__(self):
        super().__init__('orange', 2)

    def get_grades(self, course):
        grades = super().get_grades("Hufflepuff", course)
        self.grades[course] = super().get_normalized_mean(grades)

    def set_label(self, course):
        super().plot(0, self.grades[course], label="Hufflepuff")


class Ravenclaw(Hogwarts):
    
    grades = {}
    
    def __init__(self):
        super().__init__('blue', 3)

    def get_grades(self, course):
        grades = super().get_grades("Ravenclaw", course)
        self.grades[course] = super().get_normalized_mean(grades)

    def set_label(self, course):
        super().plot(0, self.grades[course], label="Ravenclaw")


class Slytherin(Hogwarts):
    
    grades = {}
    
    def __init__(self):
        super().__init__('green', 4)

    def get_grades(self, course):
        grades = super().get_grades("Slytherin", course)
        self.grades[course] = super().get_normalized_mean(grades)

    def set_label(self, course):
        super().plot(0, self.grades[course], label="Slytherin")