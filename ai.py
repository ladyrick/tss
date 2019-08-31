from astar import AStar


def AI(matrix, snake, candy_pos):
    path, _ = AStar(matrix, snake[0], candy_pos, walls='qzpmublrto')
    if not path:
        path, _ = AStar(matrix, snake[0], snake[-1], walls='qzpmublro')
    next_pos = path[1]
    delta = (next_pos[0] - snake[0][0], next_pos[1] - snake[0][1])
    return {
        (-1, 0): "w",
        (1, 0): "s",
        (0, -1): "a",
        (0, 1): "d",
    }[delta]
