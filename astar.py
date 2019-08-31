import heapq
import random


class Node():
    def __init__(self, H, F, pos, prev, open):
        self.H = H
        self.F = F
        self.pos = pos
        self.prev = prev
        self.open = open

    def __lt__(self, node):
        return self.H < node.H


def AStar(map, start, end, walls='#'):
    assert map[start[0]][start[1]] not in walls
    assert map[end[0]][end[1]] not in walls

    def dis(start, end):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    rows = len(map)
    cols = len(map[0])
    open_map = []
    for i in range(rows):
        open_map.append([None] * cols)
    open_heap = []
    path = []
    observed = []
    start_node = Node(dis(start, end), 0, start, None, True)
    heapq.heappush(open_heap, start_node)
    open_map[start[0]][start[1]] = start_node
    while open_heap:
        cur_node = heapq.heappop(open_heap)
        cur_node.open = False
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d in directions:
            pos_r = cur_node.pos[0] + d[0]
            pos_c = cur_node.pos[1] + d[1]
            pos = (pos_r, pos_c)
            if pos == end:
                path.append(pos)
                prev = cur_node
                while prev != None:
                    path.append(prev.pos)
                    prev = prev.prev
                return list(reversed(path)), observed
            if 0 <= pos_r < rows and 0 <= pos_c < cols and map[pos_r][pos_c] not in walls:
                if open_map[pos_r][pos_c] != None:
                    if open_map[pos_r][pos_c].open and cur_node.F + 1 < open_map[pos_r][pos_c].F:
                        open_map[pos_r][pos_c].F = cur_node.F + 1
                        open_map[pos_r][pos_c].H = open_map[pos_r][pos_c].F + dis(pos, end)
                else:
                    observed.append(pos)
                    next_node = Node(cur_node.F + 1 + dis(pos, end), cur_node.F + 1, pos, cur_node, True)
                    heapq.heappush(open_heap, next_node)
                    open_map[pos_r][pos_c] = next_node
    return path, observed


def generate(row, col):
    map = []
    for i in range(row):
        map.append([random.choice("     #") for _ in range(col)])

    start = (random.randint(0, row - 1), random.randint(0, col - 1))
    while map[start[0]][start[1]] == "#":
        start = (random.randint(0, row - 1), random.randint(0, col - 1))

    end = (random.randint(0, row - 1), random.randint(0, col - 1))
    while map[end[0]][end[1]] == "#" or end == start:
        end = (random.randint(0, row - 1), random.randint(0, col - 1))
    map[start[0]][start[1]] = "1"
    map[end[0]][end[1]] = "2"
    return map, start, end


def printmap(map):
    for row in map:
        print(''.join(row))


if __name__ == "__main__":
    row = 10
    col = 10
    map, start, end = generate(row, col)

    printmap(map)
    print(start, end)
    path, observed = AStar(map, start, end)
    print(path, observed)
    for pos in observed:
        map[pos[0]][pos[1]] = 'O'
    for pos in path[1:-1]:
        map[pos[0]][pos[1]] = '@'
    printmap(map)
