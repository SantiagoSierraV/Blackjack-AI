from enum import Enum, auto

# We use Enum because the actions are finite, make its more readable and easier to debug
class Action(Enum):
    HIT = auto()
    STAND = auto()