from uu_game.vec2 import Vec2
from uu_game.model.game import Game
from .view import View


class ErrorInfo:
    error: str

    def __init__(self):
        self.error = ""

class ErrorView(View):
    def __init__(self, error_info: ErrorInfo, *args):
        super().__init__(*args)
        self.error_info = error_info
    
    def render(self):
        self.curses_window.move(self.offset.y, self.offset.x)
        self.curses_window.clrtoeol()
        self.print(Vec2(0, 0), self.error_info.error)
        