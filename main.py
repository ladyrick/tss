import curses
import time

from screen import Screen


with Screen() as stdscr:
    stdscr.clear()

    matrix = stdscr.get_matrix()
    stdscr.update(matrix)
    stdscr.getkey()
