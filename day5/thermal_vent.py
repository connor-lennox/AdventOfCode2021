import sys


def parse_line(line):
    split = line.split(' -> ')
    p1 = split[0].split(',')
    p2 = split[1].split(',')
    return (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1]))


def is_horiz_or_vert(line):
    return line[0][0] == line[1][0] or line[0][1] == line[1][1]


def is_horiz(line):
    return line[0][1] == line[1][1]


def is_vert(line):
    return line[0][0] == line[1][0]


def is_diag(line):
    dx = abs(line[0][0] - line[1][0])
    dy = abs(line[0][1] - line[1][1])
    return dx == dy


def get_between(line):
    if is_horiz(line):
        start = min(line[0][0], line[1][0])
        stop = max(line[0][0], line[1][0])
        return [(x, line[0][1]) for x in range(start, stop+1)]
    if is_vert(line):
        start = min(line[0][1], line[1][1])
        stop = max(line[0][1], line[1][1])
        return [(line[0][0], y) for y in range(start, stop+1)]
    if is_diag(line):
        start = line[0] if line[0][0] <= line[1][0] else line[1]
        stop = line[1] if line[0][0] <= line[1][0] else line[0]
        x_range = range(start[0], stop[0]+1)
        y_range = range(start[1], stop[1]+1) if start[1] <= stop[1] else range(start[1], stop[1]-1, -1)
        return [(x, y) for (x, y) in zip(x_range, y_range)]
    return []


def count_crosses(grid):
    return sum(1 if grid[x][y] >= 2 else 0 for y in range(max_y) for x in range(max_x))


with open(sys.argv[1]) as infile:
    file_lines = infile.readlines()

lines = [parse_line(l) for l in file_lines]

max_x = max(max([p[0][0] for p in lines]), max([p[1][0] for p in lines])) + 1
max_y = max(max([p[0][1] for p in lines]), max([p[1][1] for p in lines])) + 1

grid = [[0 for _ in range(max_y)] for _ in range(max_x)]

for p in lines:
    points = get_between(p)
    for between in get_between(p):
        grid[between[0]][between[1]] += 1

print(f"Crossings: {count_crosses(grid)}")
