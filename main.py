from screen import Screen
from tss import TSS
from ai import AI

with Screen() as screen:
    tss = TSS(screen)
    tss.play(AI=AI)
