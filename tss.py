import random
import time
import collections
Candy = collections.namedtuple("Candy", "block score")


class TSS():
    candies = [Candy("口", 1), Candy("回", 2), Candy("品", 3)]
    blocks = {
        "q": "┏",  # left up
        "z": "┗",  # left down
        "p": "┓",  # right up
        "m": "┛",  # right down
        "h": "━━",  # horizontal
        "v": "┃",  # vertical
        "t": "〇",  # tail
        "w": "〇",  # head face up
        "s": "〇",  # head face down
        "a": "〇",  # head face left
        "d": "〇",  # head face right
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
                    if not self.candy:
                        self.candy = random.choice(self.candies)
                    row += self.candy.block
                else:
                    row += "  "
            matrix.append(row)
        self.screen.update(matrix)

    def set_block(self, pos, block):
        r = pos[0]
        c = pos[1]
        self.matrix[r] = self.matrix[r][:c] + block + self.matrix[r][c + 1:]

    def put_walls(self):
        rows = self.screen.rows
        cols = self.screen.cols
        self.matrix = ["q" + "h" * (self.cols - 2) + "p"]
        for i in range(1, rows - 1):
            row = "v" + "0" * (self.cols - 2) + "v"
            self.matrix.append(row)
        self.matrix.append("z" + "h" * (self.cols - 2) + "m")

    def put_snake(self):
        if not self.snake:
            r = (self.rows - 2) * random.randint(20, 80) // 100
            c = (self.cols - 2) * random.randint(20, 80) // 100
            self.snake.append([r, c])
            self.direction = random.choice(["w", "a", "s", "d"])

    def put_candy(self):
        blanks = []
        for r in range(len(self.matrix)):
            for c in range(len(self.matrix[r])):
                if self.matrix[r][c] == "0":
                    blanks.append((r, c))
        self.set_block(random.choice(blanks), "c")

    def init(self, wall=True):
        self.matrix = [""]
        self.snake = []
        self.direction = None
        self.candy = None
        self.score = 0
        self.put_walls()
        self.update()

    def move(self):
        if not self.snake:
            return True
        tail = None
        head = self.snake[0][:]
        delta = {
            "w": [-1, 0],
            "s": [1, 0],
            "a": [0, -1],
            "d": [0, 1],
        }[self.direction]
        head[0] += delta[0]
        head[1] += delta[1]
        if head[0] < 0 or head[0] >= self.rows or head[1] < 0 or head[1] >= self.cols or \
                self.matrix[head[0]][head[1]] not in "0c":
            return False
        if self.matrix[head[0]][head[1]] == "c":
            self.score += self.candy.score
            self.candy = None
            self.put_candy()
        elif len(self.snake) >= 3:
            tail = self.snake.pop()
        self.set_block(head, self.direction)
        self.set_block(self.snake[0], "t")
        tail and self.set_block(tail, "0")
        self.snake.insert(0, head)
        return True

    def turn_listener(self):
        while True:
            ch = self.screen.getch()
            keycodes = {
                119: "w",  # w
                97: "a",  # a
                115: "s",  # s
                100: "d",  # d
            }
            if ch in keycodes:
                self.direction = keycodes[ch]

    def play(self):
        self.put_snake()
        self.put_candy()
        self.update()
        self.screen.add_keyboard_listener(self.turn_listener)
        while True:
            time.sleep(0.1)
            if self.move():
                self.update()
            else:
                raise self.GameOver(self.score)
