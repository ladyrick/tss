from screen import Screen
from tss import TSS

with Screen() as screen:
    tss = TSS(screen)
    tss.init()
    tss.play()
