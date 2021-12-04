import sys

lines = []

for line in sys.stdin:
    if line.isspace():
        break
    lines.append(line.strip())

num_len = len(lines[0])

data = [0 for _ in range(num_len)]

for line in lines:
    for i, char in enumerate(line):
        if char == '1':
            data[i] += 1

print(data)

threshold = len(lines) / 2

gamma = ''.join(['1' if v > threshold else '0' for v in data])
epsilon = ''.join(['0' if v > threshold else '1' for v in data])

print(gamma)
print(epsilon)

g_int = int(gamma, 2)
e_int = int(epsilon, 2)

print(f"Gamma: {g_int}  Epsilon: {e_int}")
print(f"Product: {g_int * e_int}")
