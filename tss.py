import random
import time
import collections
import threading

Candy = collections.namedtuple("Candy", "block score")


def add_daemon(func, *args, **kwargs):
    if not callable(func):
        raise TypeError("func must be callable.")

    class Daemon(threading.Thread):
        def __init__(self, func, *args, **kwargs):
            threading.Thread.__init__(self)
            self.func = func
            self.args = args
            self.kwargs = kwargs
            self.daemon = True

        def run(self):
            self.func(*self.args, **self.kwargs)

    listener = Daemon(func, *args, **kwargs)
    listener.start()


class TSS():
    candies = [Candy("口", 1), Candy("回", 2), Candy("品", 3)]
    blocks = {
        "q": "┏━",  # left up
        "z": "┗━",  # left down
        "p": "┓ ",  # right up
        "m": "┛ ",  # right down
        "u": "━━",  # top border
        "b": "━━",  # bottom border
        "l": "┃ ",  # left border
        "r": "┃ ",  # right border
        "o": "〇",  # body
        "t": "尾",  # tail
        "w": "头",  # head face up
        "s": "头",  # head face down
        "a": "头",  # head face left
        "d": "头",  # head face right
        # "c" for candy.
        # "0" for blank.
    }

    class GameOver(Exception):
        # raise score.
        pass

    def __init__(self, screen):
        self.screen = screen
        self.rows = screen.rows
        self.cols = screen.cols // 2

    def update(self):
        matrix = []
        assert len(self.matrix) <= self.rows
        for line in self.matrix:
            assert len(line) <= self.cols
            row = ""
            for c in line:
                if c in self.blocks:
                    row += self.blocks[c]
                elif c == "c":
                    row += self.candy.block
                else:
                    row += "  "
            matrix.append(row)
        self.screen.update(matrix)

    def set_block(self, pos, block):
        self.matrix[pos[0]][pos[1]] = block

    def put_walls(self):
        self.matrix[0][0] = "q"
        self.matrix[0][self.cols - 1] = "p"
        self.matrix[self.rows - 1][0] = "z"
        self.matrix[self.rows - 1][self.cols - 1] = "m"
        for c in range(1, self.cols - 1):
            self.matrix[0][c] = "u"
            self.matrix[self.rows - 1][c] = "b"
        for r in range(1, self.rows - 1):
            self.matrix[r][0] = "l"
            self.matrix[r][self.cols - 1] = "r"

    def put_snake(self):
        if not self.snake:
            r = (self.rows - 2) * random.randint(20, 80) // 100 + 1
            c = (self.cols - 2) * random.randint(20, 80) // 100 + 1
            tail = (r, c)
            self.direction = random.choice(["w", "a", "s", "d"])
            delta = {
                "w": [-1, 0],
                "s": [1, 0],
                "a": [0, -1],
                "d": [0, 1],
            }[self.direction]
            head = (r + delta[0], c + delta[1])
            self.snake = [head, tail]
            self.matrix[head[0]][head[1]] = self.direction
            self.matrix[tail[0]][tail[1]] = "t"

    def put_candy(self):
        blanks = []
        for r in range(len(self.matrix)):
            for c in range(len(self.matrix[r])):
                if self.matrix[r][c] == "0":
                    blanks.append((r, c))
        self.candy_pos = random.choice(blanks)
        self.candy = random.choice(self.candies)
        self.set_block(self.candy_pos, "c")

    def reset(self):
        self.matrix = []
        for i in range(self.rows):
            self.matrix.append(["0"] * self.cols)
        self.snake = None
        self.direction = None
        self.candy = None
        self.candy_pos = None
        self.score = 0

    def move(self, direction):
        if not self.snake:
            return True
        tail = None
        head = self.snake[0]
        delta = {
            "w": [-1, 0],
            "s": [1, 0],
            "a": [0, -1],
            "d": [0, 1],
        }[direction]
        head = (head[0] + delta[0], head[1] + delta[1])
        candy_eaten = self.matrix[head[0]][head[1]] == "c"
        if not candy_eaten:
            tail = self.snake.pop()
            self.set_block(tail, "0")
        if head[0] < 0 or head[0] >= self.rows or head[1] < 0 or head[1] >= self.cols or \
                self.matrix[head[0]][head[1]] not in "0c":
            return False
        self.set_block(head, direction)
        self.set_block(self.snake[0], "o")
        if tail:
            self.set_block(self.snake[-1], "t")
        self.snake.insert(0, head)
        if candy_eaten:
            self.score += self.candy.score
            self.put_candy()
        return True

    def turn_listener(self):
        while True:
            ch = self.screen.getch()
            keycodes = {
                119: ("w", "ad"),  # w
                97: ("a", "ws"),  # a
                115: ("s", "ad"),  # s
                100: ("d", "ws"),  # d
            }
            if ch in keycodes:
                new_direction = keycodes[ch]
                if self.direction in new_direction[1]:
                    self.direction = new_direction[0]

    def gameover_no_update(self):
        r = self.screen.rows // 2
        c = self.screen.cols // 2 - 9
        self.screen.addstr(r - 2, c, "┏━━━━━━━━━━━━━━━━┓")
        self.screen.addstr(r - 1, c, "┃                ┃")
        self.screen.addstr(r + 0, c, "┃    GAME OVER   ┃")
        self.screen.addstr(r + 1, c, "┃                ┃")
        self.screen.addstr(r + 2, c, "┗━━━━━━━━━━━━━━━━┛")
        self.screen.move(self.screen.rows - 1, 0)
        self.screen.refresh()

    def play(self, AI=None):
        self.reset()
        self.put_walls()
        self.put_snake()
        self.put_candy()
        self.update()
        if not AI:
            add_daemon(self.turn_listener)
        while True:
            if AI:
                try:
                    self.direction = AI(self.matrix, self.snake, self.candy_pos)
                except:
                    time.sleep(3600)
                    break
                time.sleep(0.05)
            else:
                time.sleep(0.2)
            if self.move(self.direction):
                self.update()
            else:
                self.gameover_no_update()
                time.sleep(0.5)
                raise self.GameOver(self.score)
