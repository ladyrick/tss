import curses
import os
import threading


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
        if args[0] == KeyboardInterrupt:
            print("exit by user.")
            return True
        return False

    def pause(self):
        self.__screen.getch()

    def get_matrix(self):
        return ["#" * self.cols] * self.rows

    def update(self, matrix):
        for i, line in enumerate(matrix):
            self.insstr(i, 0, line)
        self.refresh()

    def __getattr__(self, item):
        return self.__screen.__getattribute__(item)

    def add_keyboard_listener(self, callback, *args, **kwargs):
        if not callable(callback):
            raise TypeError("callback must be callable.")

        class Listener(threading.Thread):
            def __init__(self, callback, *args, **kwargs):
                threading.Thread.__init__(self)
                self.callback = callback
                self.args = args
                self.kwargs = kwargs

            def run(self):
                self.callback(*self.args, **self.kwargs)

        listener = Listener(callback, *args, **kwargs)
        listener.daemon = True
        listener.start()
