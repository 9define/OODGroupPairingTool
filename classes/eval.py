# use enums
from enum import Enum


# there are only 3 possible group grades
class Eval(Enum):
    VERY_GOOD = 1
    GOOD = 2
    FAIR = 3
    BAD = 4

    # extensional equality for enums
    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    # toString for enums
    def __str__(self):
        return self.name
