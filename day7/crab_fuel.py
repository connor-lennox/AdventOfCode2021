import sys
from statistics import median, mean

with open(sys.argv[1]) as infile:
    crab_pos = [int(p) for p in infile.readline().split(',')]

# When fuel costs are constant, the median position is optimal.
part1_target = round(median(crab_pos))
part1_total_fuel = sum([abs(part1_target - p) for p in crab_pos])

print(f"P1: Aligning at Position: {part1_target}")
print(f"P1: Total Fuel to Align: {part1_total_fuel}")
print()

# Just mean did not work here... but floor(mean) does. I'm not sure why,
# but instead of messing with the math I will just brute-force to solve for
# the best position.
part2_diffs = [[abs(i - p) for p in crab_pos] for i in range(0, max(crab_pos))]
part2_fuels = [sum([d * (d+1) // 2 for d in diffs]) for diffs in part2_diffs]
part2_target = min(range(len(part2_fuels)), key=lambda i: part2_fuels[i])
part2_minfuel = part2_fuels[part2_target]

print(f"P2: Aligning at Position: {part2_target}")
print(f"P2: Total Fuel to Align: {part2_minfuel}")
