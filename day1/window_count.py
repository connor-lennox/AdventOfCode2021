import sys


readings = []

for line in sys.stdin:
    if line.isspace():
        break
    readings.append(int(line))

sums = [sum(readings[i:i+3]) for i in range(len(readings)-2)]

last_sum = -1
num_increase = -1

for v in sums:
    if v > last_sum:
        num_increase += 1
    last_sum = v


print(sums)

print(num_increase)
