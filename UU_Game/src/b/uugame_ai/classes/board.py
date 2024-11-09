import copy

from uu_game.vec2 import Vec2


class Board:
    def __init__(self, size=Vec2(4, 4), board=None):
        self.size = size
        self.board = board if board is not None else self.generate_board()

    def generate_board(self):
        board = []
        for x in range(self.size.x):
            board.append([])
            for _ in range(self.size.y):
                board[x].append([])
        return board

    def get_board(self):
        return self.board

    def get_cell(self, x, y):
        return self.board[x][y]

    def get_stone(self, x, y, z):
        return self.board[x][y][z]

    def set_cell(self, x, y, cell):
        self.board[x][y] = cell

    def set_stone(self, x, y, z, stone):
        self.board[x][y][z] = stone

    def __str__(self):
        res = ""
        for row in self.board:
            res += "|"
            for cell in row:
                res += "  " + str(cell) + "  " 
            res += "\n"

        return res #f"Board(board={self.board})"

    def __repr__(self):
        return self.__str__()

    def copy(self):
        return copy.deepcopy(self)
