import sys


EMPTY = 0
DOWN = 1
RIGHT = 2

charmap = {'.': EMPTY, 'v': DOWN, '>': RIGHT}


with open(sys.argv[1]) as infile:
    grid = [[charmap[c] for c in line.strip()] for line in infile]


WIDTH = len(grid[0])
HEIGHT = len(grid)


def converged(prev, cur):
    return prev == cur


def can_move(cur, x, y):
    target = cur[y][x]
    if target == DOWN:
        px, py = x, (y + 1) % HEIGHT
        return cur[py][px] == EMPTY
    if target == RIGHT:
        px, py = (x + 1) % WIDTH, y
        return cur[py][px] == EMPTY

    return False


def step(cur):
    new = [[cur[y][x] for x in range(WIDTH)] for y in range(HEIGHT)]
    
    # Move eastward herd
    for x in range(WIDTH):
        for y in range(HEIGHT):
            target = new[y][x]
            if can_move(cur, x, y) and target == RIGHT:
                px, py = (x + 1) % WIDTH, y
                new[py][px] = RIGHT
                new[y][x] = EMPTY
    
    new2 = [[new[y][x] for x in range(WIDTH)] for y in range(HEIGHT)]

    # Move southward herd
    for x in range(WIDTH):
        for y in range(HEIGHT):
            target = new[y][x]
            if can_move(new, x, y) and target == DOWN:
                    px, py = x, (y + 1) % HEIGHT
                    new2[py][px] = DOWN
                    new2[y][x] = EMPTY

    return new2


num_steps = 0

while(True):
    old = grid
    grid = step(grid)
    num_steps += 1
    if converged(old, grid):
        print(f"Part 1: Num Steps: {num_steps}")
        break
