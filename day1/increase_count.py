import sys


last_reading = 0
num_increase = -1

for line in sys.stdin:
    if line.isspace():
        break
    v = int(line)
    if v > last_reading:
        num_increase += 1
    last_reading = v

print(num_increase)
