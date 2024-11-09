from uu_game.model.game import Game
from ..classes.color import Color
from ..classes.board import Board


def remaining_stones(board: Board) -> dict[tuple[Color, bool], int]:
    """
    This function returns the number of remaining stones for each color
    :param board: the actual state of the board
    :return: dictionary of remaining stones for each color
    """
    counts: dict[tuple[Color, bool], int] = {(Color.WHITE, False): 16, (Color.WHITE, True): 5, (Color.BLACK, False): 16, (Color.BLACK, True): 5}

    # traversing the each cell of the board
    for x in range(board.size.x):
        for y in range(board.size.y):
            corresponding_cell = board.get_cell(x, y)
            number_of_stones_in_cell = len(corresponding_cell)

            # loop through each stone in the cell
            for z in range(number_of_stones_in_cell):
                stone = board.get_cell(x, y)[z]
                counts[(stone.color, stone.is_standing)] -= 1

    return counts
