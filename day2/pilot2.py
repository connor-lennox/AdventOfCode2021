import sys


lines = []

for line in sys.stdin:
    if line.isspace():
        break
    lines.append(line)

horiz = 0
depth = 0
aim = 0

for line in lines:
    p = line.split()
    amt = int(p[1])
    if p[0] == 'forward':
        horiz += amt
        depth += aim * amt
    elif p[0] == 'up':
        aim -= amt
    elif p[0] == 'down':
        aim += amt

print(f"Horiz: {horiz} Depth: {depth}  Product: {horiz * depth}")
