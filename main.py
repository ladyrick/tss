import curses
import time

from screen import Screen

with Screen() as screen:
    from tss import TSS
    tss = TSS(screen)
    tss.init()
    screen.pause()
