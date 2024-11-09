from ...classes.board import Board

def get_adjacent(board: Board, x: int, y: int) -> list[tuple[int, int]]:
    """
    this function gives all coordinates in a list of the horizontal and vertical neighbors
    :param x: the actual x-coordinate
    :param y: the actual y-coordinate
    :return: a list of all neighbors in [x,y] coordinates
    """
    neighbors = []
    if x == 0:
        neighbors.append((1, y))
    elif x == board.size.x - 1:
        neighbors.append((board.size.x-2, y))
    else:
        neighbors.append((x - 1, y))
        neighbors.append((x + 1, y))

    if y == 0:
        neighbors.append((x, 1))
    elif y == board.size.y - 1:
        neighbors.append((x, board.size.y-2))
    else:
        neighbors.append((x, y - 1))
        neighbors.append((x, y + 1))

    return neighbors
