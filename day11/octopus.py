import sys


# Read current ocotpi state from file
with open(sys.argv[1]) as infile:
    octopi = [[int(c) for c in line.strip()] for line in infile]


# Generator for adjacent tiles in grid, including diagonals
def adjacent(i, j):
    for di in range(-1, 2):
        for dj in range(-1, 2):
            if 0 <= i+di <= 9 and 0 <= j+dj <= 9:
                yield (i+di, j+dj)


def flash_iteration():
    # Start by increasing the level of all octopi by 1
    # Also find all octopi that have a level of at least 9
    # Closed list is list of all octopi which have already flashed
    open = []
    closed = set()

    for i in range(len(octopi)):
        for j in range(len(octopi[i])):
            octopi[i][j] += 1
            if octopi[i][j] > 9:
                open.append((i, j))
                closed.add((i, j))

    # Use a "floodfill" algorithm to find chain reactions of flashes
    while len(open) > 0:
        # Considering one location
        (x, y) = open.pop()
        for (ax, ay) in adjacent(x, y):
            if (ax, ay) not in closed:
                octopi[ax][ay] += 1
                if octopi[ax][ay] > 9 and (ax, ay) not in open:
                    open.append((ax, ay))
                    closed.add((ax, ay))

    # Reset value of octopi that flashed this round
    for (x, y) in closed:
        octopi[x][y] = 0

    return len(closed)


# Part 1: Iterate through 100 times, counting flashes
flash_sum = 0
num_iterations = 100
for _ in range(num_iterations):
    flash_sum += flash_iteration()

print(f"Part 1: Total flashes after {num_iterations} iterations: {flash_sum}")


# Part 2: Find first round where all flash together

# Returns true if all octopi flashed in the previous round
def all_flashed():
    return all([octopi[i][j] == 0 for i in range(len(octopi)) for j in range(len(octopi[i]))])


# Reset octopi state by re-reading file
with open(sys.argv[1]) as infile:
    octopi = [[int(c) for c in line.strip()] for line in infile]

iter_count = 0
while not all_flashed():
    flash_iteration()
    iter_count += 1

print(f"Part 2: First round where all flash together: {iter_count}")