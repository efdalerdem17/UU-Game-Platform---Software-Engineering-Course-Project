from ..classes.stone import Stone
from ..classes.color import Color
from ..classes.board import Board
from .utils.helper_functions import get_adjacent
import random


def place_initial_stone(board: Board, opponent_color: Color) -> Board:
    """
    Place the initial stone of the opponent on the board.
    :param board: the board to place the stone on
    :param opponent_color: the color of the opponent
    :return: the board with the initial stone placed
    """

    # Choose one of the following two options randomly:
    select_mode = random.choice([True, False])
    if select_mode:
        # 1. place the stone randomly on the board, either standing or lying based on randomness
        x = random.randint(0, 3)
        y = random.randint(0, 3)

        # if a standing stone is already on this cell, select an adjacent cell
        if len(board.get_cell(x, y)) > 0:
            if board.get_cell(x, y)[-1].is_standing:
                neighbor = random.choice(get_adjacent(board, x, y))
                x = neighbor[0]
                y = neighbor[1]

        is_standing = random.choice([True, False])
        board.get_board()[x][y].append(Stone(opponent_color, is_standing))
    else:
        # 2. place a stone standing in on of the corners, pick the corner randomly
        x = random.choice([0, 3])
        y = random.choice([0, 3])

        # if a standing stone is already on this cell, select another corner
        if len(board.get_cell(x, y)) > 0:
            if board.get_cell(x, y)[-1].is_standing:
                x = 0 if x == 3 else 3

        board.get_board()[x][y].append(Stone(opponent_color, True))

    return board
