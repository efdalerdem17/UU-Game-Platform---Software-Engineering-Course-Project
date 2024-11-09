from enum import Enum


class Mode(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2


def print_color(mode: Mode):
    if mode == Mode.EASY:
        return "EASY"
    elif mode == Mode.MEDIUM:
        return "MEDIUM"
    elif mode == Mode.HARD:
        return "HARD"
    else:
        return None
