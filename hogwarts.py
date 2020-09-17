import matplotlib.pyplot as plt

from describe import Data, Students, Features
from DSCRB.calculations import mean_

class Hogwarts:

    def __init__(self, name, color, position):
        self.name = name
        self.color = color
        self.position=position
        self.grades = {}
        self.normalized_average = {}

    def get_grades(self, course, normalized_average=False):
        course_nb = Features.titles.index(course)
        grades = Students.get_one_feature(course_nb, self.name)
        self.grades[course] = grades
        if normalized_average:
            self.normalize_grades(mean_(grades), course, course_nb)

    def normalize_grades(self, average, course, course_nb, max_range=100):
        try:
            max_grade = Data.info[course_nb]["Max"]
            min_grade = Data.info[course_nb]["Min"]
        except:
            return

        try:
            if max_grade > 0:
                normalized = (average * max_range) // max_grade
            elif max_grade < 0:
                normalized = (average * -max_range) // min_grade
            self.normalized_average[course] = normalized
        except:
            pass

    def plot(self, course, score, label=None):
        plt.bar(course + self.position, score, color=self.color, width=1, label=label)

    def set_label(self, course):
        self.plot(0, self.normalized_average[course], label=self.name)

class Gryffindor(Hogwarts):

    def __init__(self):
        super().__init__("Gryffindor", 'maroon', 1)

class Hufflepuff(Hogwarts):
    
    def __init__(self):
        super().__init__("Hufflepuff", 'orange', 2)

class Ravenclaw(Hogwarts):
    
    def __init__(self):
        super().__init__("Ravenclaw", 'blue', 3)

class Slytherin(Hogwarts):
    
    def __init__(self):
        super().__init__("Slytherin", 'green', 4)