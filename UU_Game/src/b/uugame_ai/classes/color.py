from enum import Enum


class Color(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2


def print_color(color: Color):
    if color == Color.BLACK:
        return "BLACK"
    elif color == Color.WHITE:
        return "WHITE"
    else:
        return None
