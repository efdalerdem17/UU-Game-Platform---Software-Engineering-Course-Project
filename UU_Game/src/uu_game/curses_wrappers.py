import curses
from typing import Union


def _init_hex_color(n: int, hex: str):
    scale = 1000 / 255
    r = int(hex[1:3], 16)
    g = int(hex[3:5], 16)
    b = int(hex[5:7], 16)
    curses.init_color(n, round(r * scale), round(g * scale), round(b * scale))

color_ids: dict[Union[tuple[str, str], str], int] = {}
next_color_id = 1
next_color_pair_id = 1

def _get_color(color: str) -> int:
    global next_color_id
    if color not in color_ids:
        _init_hex_color(next_color_id, color)
        color_ids[color] = next_color_id
        next_color_id += 1
    return color_ids[color]

def get_color_pair(fg: str, bg: str) -> int:
    """
    Gets a Curses text attribute for setting the foreground and background colors
    """
    global next_color_pair_id
    if (fg, bg) not in color_ids:
        curses.init_pair(next_color_pair_id, _get_color(fg), _get_color(bg))
        color_ids[(fg, bg)] = curses.color_pair(next_color_pair_id)
        next_color_pair_id += 1
    return color_ids[(fg, bg)]

def start_curses(curses_window: "curses.window"):
    # Initialize the screen
    curses.initscr()
    # Turn off automatic echoing of keys to the screen
    curses.noecho()
    # React to keys instantly without needing the Enter key
    curses.cbreak()
    # Enable color support
    curses.start_color()
    # Generate events for more keys
    curses_window.keypad(True)
    # Hide cursor
    curses.curs_set(0)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    # No need to wait for a double click
    curses.mouseinterval(0)

def exit_curses(curses_window: "curses.window"):
    # Restore the terminal to its original operating mode
    curses.nocbreak()
    curses_window.keypad(False)
    curses.echo()
    curses.endwin()