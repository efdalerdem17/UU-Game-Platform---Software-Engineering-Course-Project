from ..classes.color import Color
from ..classes.board import Board


def is_board_valid(board_state: Board, player_color: Color) -> bool:
    """
    This functions checks if the provided board is valid or not
    :param board_state: the actual state of the board
    :return: boolean if the board is valid
    """

    # number of stones in the board
    black_stone_count = 0
    white_stone_count = 0

    # traversing the each cell of the board
    for x in range(board_state.size.x):
        for y in range(board_state.size.y):
            corresponding_cell = board_state.get_cell(x, y)
            number_of_stones_in_cell = len(corresponding_cell)
            # to check if there is a standing stone in the cell
            is_standing = False

            # loop through each stone in the cell
            for z in range(number_of_stones_in_cell):
                if is_standing:
                    # board is not valid because there is a stone that is on the top of a standing stone
                    return False
                elif board_state.get_cell(x, y)[z].is_standing == True:
                    # if our stone is standing, make the is_standing condition true for future checks
                    is_standing = True

                if board_state.get_cell(x, y)[z].color == Color.BLACK:
                    # if corresponding stone is black, increase the counter for the black stone by 1.
                    black_stone_count += 1
                else:
                    white_stone_count += 1

    # after counting all the stones in the board, check if the number of stones of each color are above 15 or not.
    if black_stone_count > 15 or white_stone_count > 15:
        return False

    # if there are more than 1 black stones and no white stones or vice versa, then the board is not valid
    if black_stone_count > 1 and white_stone_count == 0:
        return False
    if white_stone_count > 1 and black_stone_count == 0:
        return False

    # check if the opponent placed the wrong initial stone
    if player_color == Color.BLACK and black_stone_count == 0 and white_stone_count == 1:
        return False
    if player_color == Color.WHITE and white_stone_count == 0 and black_stone_count == 1:
        return False

    return True
