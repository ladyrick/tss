import curses
import os


class Screen():
    def __init__(self, w_char=False):
        self.w_char = w_char
        cols, rows = os.get_terminal_size()
        self.rows = rows
        self.cols = cols

    def __enter__(self):
        self.__screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.__screen.keypad(True)
        return self

    def __exit__(self, *args):
        curses.nocbreak()
        self.__screen.keypad(False)
        curses.echo()
        curses.endwin()
        curses.curs_set(1)
        return False

    def get_matrix(self):
        return ["#" * self.cols] * self.rows

    def update(self, matrix):
        assert len(matrix) == self.rows
        for i, line in enumerate(matrix):
            assert len(line) == self.cols
            self.insstr(i, 0, line)
        self.refresh()

    def __getattr__(self, item):
        return self.__screen.__getattribute__(item)
