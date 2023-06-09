from enum import Enum

class Mode(Enum):
    EASY={
        "width": 9,
        "height": 9,
        "mines": 10
        }
    MEDIUM={
        "width": 16,
        "height": 16,
        "mines": 40
        }
    HARD={
        "width": 30,
        "height": 16,
        "mines": 99
        }

    def __getitem__(self, item):
        return self.value[item]

    def __str__(self):
        return self.name + ": " + str(self.value["width"]) + " x " + str(self.value["height"])