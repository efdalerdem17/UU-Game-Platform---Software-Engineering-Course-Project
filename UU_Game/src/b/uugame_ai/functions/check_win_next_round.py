from ..classes.color import Color
from ..classes.board import Board
from ..functions.utils.helper_functions import get_adjacent


def path_completeable(
    board: Board,
    player_color: Color,
    stones_left: int,
    path: list[tuple[int, int]],
    foi: tuple[int, int],
) -> bool:
    """
    This function checks if a path is a winning path by placing a stone or moving a stone in the missing cell.
    """

    # if a stone is left to place than the path is a winning path
    if stones_left > 0:
        return True

    # check if a neighbor can be moved to the missing cell
    neighbors = get_adjacent(board, foi[0], foi[1])
    for neighbor in neighbors:
        x = neighbor[0]
        y = neighbor[1]

        # top most stone has to be flat
        if (len(board.get_cell(x, y)) > 0) and (board.get_cell(x, y)[-1].is_standing):
            continue

        # if neighbor is in winning path, two stones of the players color have to lay on each other
        if neighbor in path:
            for i in range(len(board.get_cell(x, y)) - 1):
                if (board.get_stone(x, y, i).color == player_color) and (
                    board.get_stone(x, y, i + 1).color == player_color
                ):
                    return True

        # if neighbor is not in the winning path, the players color has to lay in top
        else:
            if (len(board.get_cell(x, y)) > 0) and (
                board.get_cell(x, y)[-1].color == player_color
            ):
                return True

    return False


def check_winning_next_round(
    board: Board, color: Color, stones_left: int
) -> tuple[bool, list[tuple[int, int]], tuple[int, int]]:
    """
    This function checks if the given color can win the game in the next round
    :param board: the actual state of the board
    :param color: the color for which it is checked if the player won
    :param stones_left: int how many stones are left for this player
    :return: boolean if the player can win next round
    :return: winning path as a list of board coordinates
    """

    # check if player can win vertical
    startpoint_v = [(0, y) for y in range(board.size.y)]
    for point in startpoint_v:
        res, path, skipped_cell = is_winning(
            point[0], point[1], -1, -1, board, color, "v"
        )
        if res and path_completeable(board, color, stones_left, path, skipped_cell):
            return res, path, skipped_cell

    # check if player can win horizontal
    startpoint_h = [(x, 0) for x in range(board.size.x)]
    for point in startpoint_h:
        res, path, skipped_cell = is_winning(
            point[0], point[1], -1, -1, board, color, "h"
        )
        if res and path_completeable(board, color, stones_left, path, skipped_cell):
            return res, path, skipped_cell

    # case if player did not won yet
    return False, [], skipped_cell


def is_winning(
    x: int,
    y: int,
    x_old: int,
    y_old: int,
    board: Board,
    color: Color,
    direction: str,
    depth=0,
    skip_cell=(-1, -1),
) -> tuple[bool, list[tuple[int, int]], tuple[int, int]]:
    """
    Function that is recursively building a path to the other side of the board on the players stones.
    :param x: the actual x-coordinate
    :param y: the actual y-coordinate
    :param x_old: the x-coordinate from the function call before
    :param y_old: the y-coordinate from the function call before
    :param board: the actual state of the board
    :param color: the color of the player
    :param direction: the direction of the path ("v" for vertical or "h" for horizontal)
    :param skip_cell: the cell which is left for winning the game. On this cell a stone has to be placed for winning the game
    :param depth: the depth of the recursion, because the longest winning path is 7
    :return: True if other side of direction is reached otherwise False
    :return: the path to other side or empty list
    :return: the skip_cell which is used
    """

    # max depth is reached
    if depth == 8:
        return False, [], skip_cell

    # there is a stone on the cell
    if len(board.get_cell(x, y)) != 0:

        # stone on cell is standing
        if board.get_cell(x, y)[-1].is_standing:
            return False, [], skip_cell

        # other side is reached in vertical way
        if (
            (direction == "v")
            and (x == 3)
            and (board.get_cell(x, y)[-1].color == color)
        ):
            return True, [(x, y)], skip_cell

        # other side is reached in horizontal way
        if (
            (direction == "h")
            and (y == 3)
            and (board.get_cell(x, y)[-1].color == color)
        ):
            return True, [(x, y)], skip_cell

        # Other side is reached with using skip cell
        if (direction == "v") and (x == 3) and skip_cell[0] == -1:
            return True, [(x, y)], (x, y)

        # other side is reached in horizontal way
        if (direction == "h") and (y == 3) and skip_cell[0] == -1:
            return True, [(x, y)], (x, y)

        # stone on cell has wrong color
        if board.get_cell(x, y)[-1].color != color:
            # fail if skip_cell is used otherwise set skip_cell
            if skip_cell[0] > -1:
                return False, [], skip_cell
            else:
                skip_cell = (x, y)

    # board on that cell is empty
    if len(board.get_cell(x, y)) == 0:
        # fail if skip_cell is used otherwise set skip_cell
        if skip_cell[0] > -1:
            return False, [], skip_cell
        if (direction == "h") and (y == 3):
            return True, [(x, y)], (x, y)
        if (direction == "v") and (x == 3):
            return True, [(x, y)], (x, y)
        else:
            skip_cell = (x, y)

    neighbors = get_adjacent(board, x, y)

    # iterate over all neighbors and recursively call function with new coordinates
    for neighbor in neighbors:
        x_new = neighbor[0]
        y_new = neighbor[1]

        # cell was visited before and therefor is skipped
        if (x_new == x_old) and (y_new == y_old):
            continue
        res, path, new_skip_cell = is_winning(
            x_new, y_new, x, y, board, color, direction, depth + 1, skip_cell
        )
        if res:
            return True, path + [(x, y)], new_skip_cell

    return False, [], new_skip_cell
