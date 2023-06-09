from enum import Enum


class State(Enum):
    REVEALED = "0"
    EXPLODED = "💥"
    HIDDEN = ""
    FLAGGED = "🚩"
    MINE = "💣"

    def __str__(self):
        return self.value
