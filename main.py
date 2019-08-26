import curses
import time

from screen import Screen


with Screen() as stdscr:
    stdscr.clear()
    args = {
        "num": 0,
        "direction": "+",
    }

    def change_args(args):
        while True:
            key = stdscr.getch()
            if 48 <= key <= 57:  # keyboard 0-9
                args["num"] = key - 48
            elif key == 61:  # keyboard +
                args["direction"] = "+"
            elif key == 45:  # keyboard -
                args["direction"] = "-"

    stdscr.add_keyboard_listener(change_args, args)
    while True:
        matrix = stdscr.rows * [stdscr.cols * str(args["num"])]
        stdscr.update(matrix)
        args["num"] = (args["num"] + (1 if args["direction"] == "+" else -1)) % 10
        time.sleep(0.5)
