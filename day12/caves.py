from os import openpty
import sys


with open(sys.argv[1]) as infile:
    in_edges = infile.readlines()


def can_visit(path, cave):
    return cave.isupper() or cave not in path


def can_double_visit(path, cave):
    return cave != "start" and cave != "end" and path[1]


edges = {}

for line in in_edges:
    a, b = [c.strip() for c in line.split('-')]
    if a not in edges:
        edges[a] = []
    if b not in edges:
        edges[b] = []
    edges[a].append(b)
    edges[b].append(a)

# Prep lists
open_paths = [("start",)]
closed_paths = set()
complete_paths = []

# Go until no paths left to explore
while len(open_paths) > 0:
    # Get the current subpath
    cur = open_paths.pop()
    # Find candidate locations to visit
    candidates = edges[cur[-1]]
    for candidate in candidates:
        # Check to make sure we aren't duplicating a small cave
        if can_visit(cur, candidate):
            # Construct new path, handle reaching end
            new_path = tuple(list(cur) + [candidate])
            if candidate != "end":
                if new_path not in open_paths and new_path not in closed_paths:
                    open_paths.append(new_path)
            else:
                if new_path not in closed_paths:
                    complete_paths.append(new_path)
            closed_paths.add(new_path)

# Part 1: The number of paths that lead to "end"
print(f"Part 1: Total Paths Found: {len(complete_paths)}")



# Part 2: Can now visit a single small cave twice.
# To allow this, paths are now a tuple (path, can_duplicate)

# Prep lists again
open_paths = [(("start",), True)]
closed_paths = set()
complete_paths = []

# Mostly the same procedure as before
while len(open_paths) > 0:
    cur = open_paths.pop()
    candidates = edges[cur[0][-1]]

    for candidate in candidates:
        if can_visit(cur[0], candidate):
            new_path = tuple(list(cur[0]) + [candidate])
            if candidate != "end":
                if new_path not in open_paths and new_path not in closed_paths:
                    open_paths.append((new_path, cur[1]))
            else:
                if new_path not in closed_paths:
                    complete_paths.append(new_path)
            closed_paths.add(new_path)
        elif can_double_visit(cur, candidate):
            new_path = tuple(list(cur[0]) + [candidate])
            if new_path not in open_paths and new_path not in closed_paths:
                open_paths.append((new_path, False))


# Part 1: The number of paths that lead to "end", with one optional duplicate small cave
print(f"Part 2: Total Paths Found: {len(complete_paths)}")