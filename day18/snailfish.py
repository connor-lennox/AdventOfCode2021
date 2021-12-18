import sys
from math import floor, ceil


def find_next(line, idx):
    i = idx
    while not line[i].isdigit(): 
        i += 1
        if i >= len(line):
            return None
    j = i
    while line[j].isdigit():
        j += 1
        if j >= len(line):
            break
    return (i, j)


def find_prev(line, idx):
    j = idx
    while not line[j].isdigit():
        j -= 1
        if j < 0:
            return None
    j += 1
    i = j-1
    while line[i].isdigit():
        i -= 1
        if i <= 0:
            break
    i += 1
    return (i, j)



def explode(line):
    depth = 0
    for i in range(len(line)):
        if line[i] == '[':
            depth += 1
            # We may have to explode this pair
            if depth > 4:
                # String parse to find the two numbers involved in this explode
                c_idx = line.find(',', i)
                pair_end = line.find(']', c_idx)
                left = int(line[i+1:c_idx])
                right = int(line[c_idx+1:pair_end])
                
                # Find the previous/next numbers to add to
                prev_span = find_prev(line, i)
                next_span = find_next(line, pair_end)

                # Construct new numbers
                new_prev = int(line[prev_span[0]:prev_span[1]]) + left if prev_span != None else None
                new_next = int(line[next_span[0]:next_span[1]]) + right if next_span != None else None

                # Build string portions
                left_portion = f"{line[:prev_span[0]]}{new_prev}{line[prev_span[1]:i]}" if prev_span != None else line[:i]
                right_portion = f"{line[pair_end+1:next_span[0]]}{new_next}{line[next_span[1]:]}" if next_span != None else line[pair_end+1:]

                # Recombine into new string
                return "".join([left_portion, "0", right_portion]), True

        elif line[i] == ']':
            depth -= 1

    return line, False


def split(line):
    for i in range(len(line)):
        # If we hit a number, find the full span of the number
        if line[i].isdigit():
            digitend = i+1
            while line[digitend].isdigit(): digitend += 1

            # If the number is greater than 9, split it
            num = int(line[i:digitend])
            if num >= 10:
                left, right = floor(num/2), ceil(num/2)
                return f"{line[:i]}[{left},{right}]{line[digitend:]}", True

    return line, False


def reduce(line: str):
    while True:
        # First check for explodes
        line, res = explode(line)
        if res:
            continue

        # Then check splits
        line, res = split(line)
        if res:
            continue

        # If we get this far, no changes were made (done)
        break

    return line


def add(left, right):
    return f"[{left},{right}]"


def _magnitude(line, idx):
    # Recursive magnitude implementation
    if line[idx] == '[':
        # Process left and right sides of pair, then calculate value
        left, idx = _magnitude(line, idx+1)
        right, idx = _magnitude(line, idx+1)
        return 3 * left + 2 * right, idx
    else:
        # Process this value, then skip any closing brackets and comma
        i = idx
        while line[i].isdigit(): i += 1
        j = i
        while line[j] == ']': 
            j += 1
            if j >= len(line): break
        return int(line[idx:i]), j


def magnitude(line):
    return _magnitude(line, 0)[0]


with open(sys.argv[1]) as infile:
    numbers = [line.strip() for line in infile]


# Part 1: Sum all numbers, find magnitude
total = numbers[0]
print(total)
for num in numbers[1:]:
    total = add(total, num)
    total = reduce(total)
    print(total)

final_mag = magnitude(total)

print(f"Final Magnitude: {final_mag}")


# Part 2: Sum every pair, find magnitude
max_mag = 0
for x in numbers:
    for y in numbers:
        max_mag = max(max_mag, magnitude(reduce(add(x, y))))

print(f"Highest Pair Magnitude: {max_mag}")
