class TSS():
    def __init__(self, screen):
        self.screen = screen

    def draw_box(self):
        rows = self.screen.rows
        cols = self.screen.cols
        corner_c = {
            "lu": "◢ ",
            "ru": "◣ ",
            "ld": "◥ ",
            "rd": "◤ ",
        }
        line_c = {
            "hor": "██",
            "ver": "██"
        }
        matrix = [corner_c["lu"] + line_c["hor"] * (cols // 2 - 2) + corner_c["ru"]]
        for i in range(1, rows - 1):
            row = line_c["ver"] + "  " * (cols // 2 - 2) + line_c["ver"]
            matrix.append(row)
        matrix.append(corner_c["ld"] + line_c["hor"] * (cols // 2 - 2) + corner_c["rd"])
        self.screen.update(matrix)

    def init(self):
        self.draw_box()
