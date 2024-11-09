from ..classes.board import Board
from ..classes.color import Color
from ..classes.stone import Stone
import random
import copy


def can_stone_be_placed_on_cell(cell: list[Stone]) -> bool:
    """
    Check whether a stone can be placed on a cell.
    :param stone: the stone to place
    :param cell: the cell to place the stone on
    :return: True if the stone can be placed, False otherwise
    """

    return len(cell) == 0 or cell[-1].is_standing == False


def analyze_adjacent_cell(
    tmp_board: Board,
    x: int,
    y: int,
    x_before: int,
    y_before: int,
    player_color: Color,
    stack: list[Stone],
) -> list[Board]:
    """
    Analyze an adjacent cell and check if the stack can be placed on it.
    :param board: the board to get the possible moves for
    :param x: the x coordinate of the stack
    :param y: the y coordinate of the stack
    :param x_before: the x coordinate from the recursion before, prevents moving stack back
    :param y_before: the y coordinate from the recursion before, prevents moving stack back
    :param player_color: the color of the player
    :return: a list of all possible moves
    """

    cell_list = tmp_board.get_cell(x, y)
    if not can_stone_be_placed_on_cell(cell_list):
        return []

    possible_moves = []
    copied_stack = copy.deepcopy(stack)

    # place the stack as is on the adjacent cell
    move = tmp_board.copy()
    move.get_cell(x, y).extend(copied_stack)
    possible_moves.append(move)

    if len(copied_stack) > 1:
        # check for options to split the stack and continuing the move
        tmp_board.get_cell(x, y).append(copied_stack.pop(0))
        possible_moves += possible_moves_for_stack(
            tmp_board, x, y, x_before, y_before, player_color, copied_stack
        )

    return possible_moves


def check_adjacent_cells(
    tmp_board: Board,
    x: int,
    y: int,
    x_before: int,
    y_before: int,
    player_color: Color,
    stack: list[Stone],
    forbid_walk_back: bool,
) -> list[Board]:
    """
    Get all possible moves for a stack on the board.
    :param board: the board to get the possible moves for
    :param x: the x coordinate of the stack
    :param y: the y coordinate of the stack
    :param x_before: the x coordinate from the recursion before, prevents moving stack back
    :param y_before: the y coordinate from the recursion before, prevents moving stack back
    :return: a list of all possible moves
    """

    possible_moves = []

    if (x > 0) and ((x - 1) != x_before):
        possible_moves += analyze_adjacent_cell(
            tmp_board.copy(),
            x - 1,
            y,
            x if forbid_walk_back else -1,
            y if forbid_walk_back else -1,
            player_color,
            stack,
        )

    if (x < 4) and ((x + 1) != x_before):
        possible_moves += analyze_adjacent_cell(
            tmp_board.copy(),
            x + 1,
            y,
            x if forbid_walk_back else -1,
            y if forbid_walk_back else -1,
            player_color,
            stack,
        )

    if (y > 0) and ((y - 1) != y_before):
        possible_moves += analyze_adjacent_cell(
            tmp_board.copy(),
            x,
            y - 1,
            x if forbid_walk_back else -1,
            y if forbid_walk_back else -1,
            player_color,
            stack,
        )

    if (y < 4) and ((y + 1) != y_before):
        possible_moves += analyze_adjacent_cell(
            tmp_board.copy(),
            x,
            y + 1,
            x if forbid_walk_back else -1,
            y if forbid_walk_back else -1,
            player_color,
            stack,
        )

    return possible_moves


def possible_moves_for_stack(
    board,
    x,
    y,
    x_before,
    y_before,
    player_color,
    stack,
    replace_cell_stack=False,
    forbid_walk_back=False,
):
    possible_moves = []

    # iterate over all stones and check if they can be placed on the cell
    max_from_stack = min(5, len(stack)-1)
    for z in range(max_from_stack):
        z = len(stack) - z + 1
        # place the lower stack on the current cell
        # and continue with the upper stack into another recursion level
        lower_stack, upper_stack = stack[:z], stack[z:]

        tmp_board = copy.deepcopy(board)

        # When the function is called initially the stack is equal to the cell stack
        # Hence we want to replace the cell stack with the lower stack
        # Afterwards we and to add the stones because they are currently not placed on the board
        if replace_cell_stack:
            tmp_board.set_cell(x, y, lower_stack)
        else:
            tmp_board.get_cell(x, y).extend(lower_stack)

        possible_moves += check_adjacent_cells(
            tmp_board,
            x,
            y,
            x_before,
            y_before,
            player_color,
            upper_stack,
            forbid_walk_back,
        )

    return possible_moves


def possible_moves(board: Board, flat_stones_left: int, standing_stones_left: int, player_color: Color) -> list[Board]:
    """
    Get all possible moves for the current board.
    :param board: the board to get the possible moves for
    :return: a list of all possible moves
    """

    possible_moving_moves = []
    possible_placing_flat_moves = []
    possible_placing_standing_moves = []

    # select n cells randomly to get generate possible moves for them
    # and prevent duplicates
    selected_cells = []
    # for i in range(4):
    #     x = random.randint(0, 3)
    #     y = random.randint(0, 3)
    #     selected_cells.append((x, y))

    for i in range(board.size.x):
        for j in range(board.size.y):
            selected_cells.append((i, j))

    # 1. place a stone on the board where no standing stone is present
    # the new stone can be placed either standing or lying
    
    flat_stone = Stone(player_color, False)
    standing_stone = Stone(player_color, True)

    for coords in selected_cells:
        cell_list = board.get_cell(coords[0], coords[1])
        if can_stone_be_placed_on_cell(cell_list):
            if flat_stones_left > 0:
                possible_placing_flat_moves.append(copy.deepcopy(board))
                possible_placing_flat_moves[-1].get_cell(coords[0], coords[1]).append(
                    flat_stone
                )
            if standing_stones_left > 0:
                possible_placing_standing_moves.append(copy.deepcopy(board))
                possible_placing_standing_moves[-1].get_cell(
                    coords[0], coords[1]
                ).append(standing_stone)

    # 2. move a stone/stack on the board to a new position
    # for each cell moved a stone has to be dropped
    for coords in selected_cells:
        cell_list = board.get_cell(coords[0], coords[1])
        possible_moving_moves += possible_moves_for_stack(
            board,
            coords[0],
            coords[1],
            -1,  # an origin that does not exists for the first stack move
            -1,
            player_color,
            cell_list,
            replace_cell_stack=True,
            forbid_walk_back=False,
        )

    possible_moves_single = (
        possible_moving_moves
        + possible_placing_flat_moves
        + possible_placing_standing_moves
    )
    # possible_moves_double = (
    #     possible_moves_single + possible_moving_moves + possible_placing_flat_moves
    # )

    return possible_moves_single
