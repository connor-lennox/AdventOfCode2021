import sys


# Rules stored as map of tuple of characters to character
rules = {}

# Read in file
with open(sys.argv[1]) as infile:
    start_string = infile.readline().strip()
    for line in infile:
        if len(line.strip()) > 0:
            s, e = line.split("->")
            rules[tuple(s.strip())] = e.strip()


# Do 10 steps
prev_string = start_string
for _ in range(10):
    # Construct next string using rules
    next_string = "".join([f"{pair[0]}{rules[pair]}" for pair in zip(prev_string[:-1], prev_string[1:])])
    # Re-add last character
    next_string += prev_string[-1]
    prev_string = next_string

# Calculate counts of each character
counts = {c: prev_string.count(c) for c in rules.values()}

print(f"Part 1: Max Count - Min Count: {max(counts.values()) - min(counts.values())}")


# Do 40 steps - much too large to brute force like above
# Find the count of each pair in the start string
all_chars = rules.values()
pair_counts = {(c1, c2): 0 for c1 in all_chars for c2 in all_chars}

for pair in zip(start_string[:-1], start_string[1:]):
    pair_counts[pair] += 1

# 40 iterations
prev_counts = pair_counts
for _ in range(40):
    # Each pair (A, B) becomes a pair of (A, C) and (C, B)
    next_counts = {(c1, c2): 0 for c1 in all_chars for c2 in all_chars}
    for k in prev_counts:
        gen = rules[k]
        next_counts[(k[0], gen)] += prev_counts[k]
        next_counts[(gen, k[1])] += prev_counts[k]
    prev_counts = next_counts
    
# The count of each character is the sum of pairs where it is the first character,
# With an additional +1 for the final character in the string
counts = {c: 0 for c in all_chars}
for k in prev_counts:
    counts[k[0]] += prev_counts[k]
counts[start_string[-1]] += 1
print(f"Part 2: Max Count - Min Count: {max(counts.values()) - min(counts.values())}")