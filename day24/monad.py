# Extracted from input
x_add = [14, 15, 12, 11, -5, 14, 15, -13, -16, -8, 15, -8, 0, -4]
y_add = [12, 7, 1, 2, 4, 15, 11, 5, 3, 9, 2, 3, 3, 11]
z_div = [1, 1, 1, 1, 26, 1, 1, 26, 26, 26, 1, 26, 26 ,26]

# Matching push/pop pairs
pairs = []
stack = []
for i in range(len(z_div)):
    if z_div[i] == 1:
        stack.append(i)
    else:
        pairs.append((stack.pop(), i))

# Solve largest model number
m1 = [0] * 14
for pair in pairs:
    diff = y_add[pair[0]] + x_add[pair[1]]
    m1[pair[0]] = 9 - max(0, diff)
    m1[pair[1]] = m1[pair[0]] + diff

print(f'Part 1: Largest Model Number: {"".join([str(m) for m in m1])}')

# Solve smallest model number
m2 = [0] * 14
for pair in pairs:
    diff = y_add[pair[0]] + x_add[pair[1]]
    m2[pair[0]] = max(1, 1 - diff)
    m2[pair[1]] = m2[pair[0]] + diff

print(f'Part 2: Smallest Model Number: {"".join([str(m) for m in m2])}')
