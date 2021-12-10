import sys
from statistics import median


OPENING = ['(', '[', '{', '<']
CLOSING = [')', ']', '}', '>']
PAIRS = {o: c for o, c in zip(OPENING, CLOSING)}
CHECKER_SCORES = {')': 3, ']': 57, '}': 1197, '>': 25137}
COMPLETE_SCORES = {'(': 1, '[': 2, '{': 3, '<': 4}


with open(sys.argv[1]) as infile:
    lines = infile.readlines()


# Part 1: Getting total syntax error score
def check_line(line):
    stack = []
    for char in line:
        if char in OPENING:
            stack.append(char)
        elif char in CLOSING:
            partner = stack.pop()
            if PAIRS[partner] != char:
                return CHECKER_SCORES[char]
    return 0


syntax_score = 0
valid_lines = []
for line in lines:
    line_score = check_line(line)
    if line_score == 0: 
        valid_lines.append(line)
    syntax_score += line_score

print(f"Part 1: Syntax Checker Score = {syntax_score}")


# Part 2: Complete all valid lines from before
def complete_line(line):
    stack = []
    for char in line:
        if char in OPENING:
            stack.append(char)
        elif char in CLOSING:
            stack.pop()
    s = 0
    stack.reverse()
    for c in stack:
        s *= 5
        s += COMPLETE_SCORES[c]
    return s


complete_score = 0
scores = [complete_line(line) for line in valid_lines]
median_score = median(scores)

print(f"Part 2: Syntax Completer Score = {median_score}")
