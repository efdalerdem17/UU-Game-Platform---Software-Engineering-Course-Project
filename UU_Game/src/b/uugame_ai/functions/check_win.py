from ..classes.color import Color
from ..classes.board import Board
from ..functions.utils.helper_functions import get_adjacent


def check_winning(board: Board, color: Color) -> tuple[bool, list[tuple[int, int]]]:
    """
    This function checks if the given color won the game
    :param board: the actual state of the board
    :param color: the color for which it is checked if the player won
    :return: boolean if game is won or not
    :return: winning path as a list of board coordinates
    """

    # check if player won vertical
    startpoint_v = [(0, y) for y in range(board.size.y)]
    for point in startpoint_v:
        res, path = is_winning(point[0], point[1], -1, -1, board, color, "v")
        if res:
            return res, path

    # check if player won horizontal
    startpoint_h = [(x, 0) for x in range(board.size.x)]
    for point in startpoint_h:
        res, path = is_winning(point[0], point[1], -1, -1, board, color, "h")
        if res:
            return res, path

    # case if player did not won yet
    return False, []


def is_winning(
    x: int,
    y: int,
    x_old: int,
    y_old: int,
    board: Board,
    color: Color,
    direction: str,
    depth=0,
) -> tuple[bool, list[tuple[int, int]]]:
    """
    Function that is recursively building a path to the other side of the board on the players stones.
    :param x: the actual x-coordinate
    :param y: the actual y-coordinate
    :param x_old: the x-coordinate from the function call before
    :param y_old: the y-coordinate from the function call before
    :param board: the actual state of the board
    :param color: the color of the player
    :param direction: the direction of the path ("v" for vertical or "h" for horizontal)
    :param depth: the depth of the recursion, because the longest winning path is 7
    :return: True if other side of direction is reached and the path otherwise False and empty list
    """

    # max depth is reached or there is no stone
    if (depth == 8) or (len(board.get_cell(x, y)) == 0):
        return False, []
    # stone has wrong color or is standing
    if (board.get_cell(x, y)[-1].color != color) or (
        board.get_cell(x, y)[-1].is_standing
    ):
        return False, []
    # other side is reached in vertical way
    if (direction == "v") and (x == board.size.x - 1):
        return True, [(x, y)]
    # other side is reached in horizontal way
    if (direction == "h") and (y == board.size.y - 1):
        return True, [(x, y)]

    neighbors = get_adjacent(board, x, y)

    # iterate over all neighbors and recursively call function with new coordinates
    for neighbors in neighbors:
        x_new = neighbors[0]
        y_new = neighbors[1]

        # cell was visited before and therefor is skipped
        if (x_new == x_old) and (y_new == y_old):
            continue
        res, path = is_winning(x_new, y_new, x, y, board, color, direction, depth + 1)
        if res:
            return True, path + [(x, y)]

    return False, []
