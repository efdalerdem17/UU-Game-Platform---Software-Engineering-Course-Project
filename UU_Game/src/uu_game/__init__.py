import curses
from uu_game.controller import Controller


def run():
    # In case of an error, this will exit the terminal "screen" first to
    # print it normally.
    curses.wrapper(lambda terminal_window: Controller(terminal_window).run())