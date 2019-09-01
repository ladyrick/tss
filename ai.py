from astar import AStar
import time


class AI():
    def __init__(self):
        self.path = []

    def get_direction(self, cur_pos, next_pos):
        delta = (next_pos[0] - cur_pos[0], next_pos[1] - cur_pos[1])
        return {(-1, 0): "w", (1, 0): "s", (0, -1): "a", (0, 1): "d"}[delta]

    def simulate(self, matrix, snake, path):
        sim_matrix = []
        for row in matrix:
            sim_matrix.append(row[:])
        move_steps = len(path) - 1
        if move_steps > len(snake):
            for pos in snake:
                sim_matrix[pos[0]][pos[1]] = "0"
            sim_matrix[path[-1][0]][path[-1][1]] = "w"
            tail = path[-len(snake) - 1]
            sim_matrix[tail[0]][tail[1]] = "t"
            for pos in path[-len(snake):-1]:
                sim_matrix[pos[0]][pos[1]] = "o"
        elif move_steps == len(snake):
            for pos in snake[1:]:
                sim_matrix[pos[0]][pos[1]] = "0"
            tail = path[0]
            sim_matrix[tail[0]][tail[1]] = "t"
            sim_matrix[path[-1][0]][path[-1][1]] = "w"
            for pos in path[1:-1]:
                sim_matrix[pos[0]][pos[1]] = "o"
        else:
            for pos in snake[- move_steps + 1:]:
                sim_matrix[pos[0]][pos[1]] = "0"
            tail = snake[-move_steps]
            sim_matrix[tail[0]][tail[1]] = "t"
            sim_matrix[snake[0][0]][snake[0][1]] = "o"
            for pos in path[:-1]:
                sim_matrix[pos[0]][pos[1]] = "o"
            sim_matrix[path[-1][0]][path[-1][1]] = "w"
        return sim_matrix, tail

    def __call__(self, matrix, snake, candy_pos):
        if self.path:
            return self.get_direction(snake[0], self.path.pop(0))
        head2candy, _ = AStar(matrix, snake[0], candy_pos, walls="qzpmublrto")
        if head2candy:
            sim_matrix, sim_tail = self.simulate(matrix, snake, head2candy)
            candy2tail, _ = AStar(sim_matrix, candy_pos, sim_tail, walls="qzpmublro")
            if candy2tail:
                self.path = head2candy[2:]
                return self.get_direction(snake[0], head2candy[1])
        head2tail, _ = AStar(matrix, snake[0], snake[-1], walls="qzpmublro")
        return self.get_direction(snake[0], head2tail[1])
