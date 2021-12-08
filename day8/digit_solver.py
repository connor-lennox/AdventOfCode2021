import sys
from collections import namedtuple


Display = namedtuple("Display", ['signal', 'output'])


def process_line(line):
    # Process a line of (signal | output) to a Display tuple
    signal, output = line.split('|')
    return Display([set(c for c in s.strip()) for s in signal.strip().split(' ')], 
                    [set(c for c in o.strip()) for o in output.strip().split(' ')])

with open(sys.argv[1]) as infile:
    displays = [process_line(line) for line in infile]


# Part 1: find out how many times 1, 4, 7, or 8 appear in all the outputs

# How many segments are lit for each number? (These are all unique across all 10 digits)
len_1478 = {2: 1, 4: 4, 3: 7, 7: 8}

num_1478s = sum([1 for display in displays for num in display.output if len(num) in len_1478])
print(f"Number of 1, 4, 7, 8 in outputs: {num_1478s}")



# Part 2: actually identify which combo corresponds to each digit

# The setup: how many segments does each number share with 1, 4, 7, and 8?
shared_segments = {
    (2, 2, 2, 2): '1',
    (1, 2, 2, 5): '2',
    (2, 3, 3, 5): '3',
    (2, 4, 2, 4): '4',
    (1, 3, 2, 5): '5',
    (1, 3, 2, 6): '6',
    (2, 2, 3, 3): '7',
    (2, 4, 3, 7): '8',
    (2, 4, 3, 6): '9',
    (2, 3, 3, 6): '0'
}

baselines = [1, 4, 7, 8]

all_numbers = []
for display in displays:
    # Keep track of digit -> set(character) ground truth
    truth = {}

    # First pass: find the combos for 1, 4, 7, and 8:
    for num in display.signal:
        if len(num) in len_1478:
            truth[len_1478[len(num)]] = num

    # Second pass: solve the output
    output_digits = []
    for num in display.output:
        overlaps = tuple(len(num.intersection(truth[s])) for s in baselines)
        output_digits.append(shared_segments[overlaps])
    all_numbers.append(int("".join(output_digits)))


print(f"Sum of all output numbers: {sum(all_numbers)}")
