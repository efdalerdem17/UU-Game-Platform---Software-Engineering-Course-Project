import curses
from typing import Optional
from uu_game.curses_wrappers import get_color_pair
from uu_game.vec2 import Vec2
from .common import BACKGROUND_COLOR, BORDER_COLOR, TEXT_COLOR


BORDER_LIGHT_CENTERED = "┌└┐┘││──"
BORDER_HALF_BLOCKS = "▗▝▖▘▐▌▄▀"
BORDER_BALANCED_EDGES = "    ▐▌▁▔"
BORDER_BALANCED_EDGES2 = "▐▐▌▌▐▌▔▂"
class View:
    """
    Base class of all views, not to be instantiated directly.
    """

    def __init__(self, curses_window: "curses.window", offset: Vec2, size: Vec2 = Vec2(1, 1)):
        self.curses_window = curses_window
        self.offset = offset
        self.size = size
        self.default_colors = (TEXT_COLOR, BACKGROUND_COLOR)

    def set_char(self, pos: Vec2, char: str, colors: Optional[tuple[str, str]] = None, underline = False):
        """
        Place a character `char` at `pos` with hexadecimal foreground and background `colors`.
        """
        try:
            text_attributes = get_color_pair(*(colors or self.default_colors))
            if underline:
                text_attributes |= curses.A_UNDERLINE
            self.curses_window.addch(
                self.offset.y + pos.y, self.offset.x + pos.x,
                char, text_attributes)
        except curses.error:
            # bottom left corner always errors even though the character is updated
            pass

    def print(self, offset: Vec2, string: str, colors: Optional[tuple[str, str]] = None, bold = False):
        """
        Print a string at `offset` optionally using a specific curses color.
        """
        text_attributes = get_color_pair(*(colors or self.default_colors))
        if bold:
            text_attributes |= curses.A_BOLD
        try:
            self.curses_window.addstr(
                offset.y + self.offset.y, offset.x + self.offset.x,
                string, text_attributes)
        except curses.error:
            pass

    def border(self, chars: str, colors: Optional[tuple[str, str]] = None):
        for y in range(-1, self.size.y+1):
            for x in range(-1, self.size.x+1):
                if x == -1 and y == -1:
                    char = 0
                elif x == -1 and y == self.size.y:
                    char = 1
                elif x == self.size.x and y == -1:
                    char = 2
                elif x == self.size.x and y == self.size.y:
                    char = 3
                elif x == -1:
                    char = 4
                elif x == self.size.x:
                    char = 5
                elif y == -1:
                    char = 6
                elif y == self.size.y:
                    char = 7
                else:
                    continue
                self.set_char(Vec2(x, y), chars[char], self.default_colors if colors is None else colors)

    def fill(self, char: str, colors: Optional[tuple[str, str]] = None, rect: Optional[tuple[Vec2, Vec2]] = None):
        if rect is None:
            rect = (Vec2(0, 0), self.size)
        for y in range(rect[1].y):
            for x in range(rect[1].x):
                self.set_char(Vec2(x, y)+rect[0], char, colors or self.default_colors)

    def render(self):
        """
        Called by the controller to render the view. All child classes should call this in their render method.
        """
        self.border(BORDER_HALF_BLOCKS, (BORDER_COLOR, BACKGROUND_COLOR))
        self.fill(' ')


