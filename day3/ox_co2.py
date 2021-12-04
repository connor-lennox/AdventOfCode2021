import sys

lines = []

for line in sys.stdin:
    if line.isspace():
        break
    lines.append(line.strip())

num_len = len(lines[0])

ox_vals = lines

def find_common(nums, i):
    ones = 0
    zeros = 0
    for n in nums:
        if n[i] == '1':
            ones += 1
        else:
            zeros += 1
    return '1' if ones >= zeros else '0'


for i in range(num_len):
    most_common = find_common(ox_vals, i)
    print(most_common)
    ox_vals = list(filter(lambda v: v[i] == most_common, ox_vals))
    print(ox_vals)
    if len(ox_vals) == 1:
        break

ox_val = ox_vals[0]


print()

co_vals = lines

for i in range(num_len):
    least_common = '0' if find_common(co_vals, i) == '1' else '1'
    print(least_common)
    co_vals = list(filter(lambda v: v[i] == least_common, co_vals))
    print(co_vals)
    if len(co_vals) == 1:
        break

co_val = co_vals[0]


print(f"O2: {ox_val}  CO2: {co_val}")

answer = int(ox_val, 2) * int(co_val, 2)
print(f"Answer: {answer}")
