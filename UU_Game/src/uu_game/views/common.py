import curses
from uu_game.curses_wrappers import get_color_pair


TEXT_COLOR = "#ffffff"
SELECTED_TEXT_COLOR = "#00ff00"
BACKGROUND_COLOR = "#302e2b"
BORDER_COLOR = "#1d1c1a"

def set_background(curses_window: "curses.window"):
    """
    Set the background of the entire window to the defaults.
    """
    curses_window.bkgd(' ', get_color_pair(TEXT_COLOR, BACKGROUND_COLOR))