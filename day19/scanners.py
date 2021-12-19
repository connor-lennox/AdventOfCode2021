import sys
from collections import namedtuple


Point = namedtuple("Point", "x y z")


def diff(p1: Point, p2: Point):
    return (p1.x - p2.x, p1.y - p2.y, p1.z - p2.z)


def manhattan(p1: Point, p2: Point):
    return sum([abs(v) for v in diff(p1, p2)])


def orientations(scanner):
    for axis1 in range(3):
        for sign1 in [1, -1]:
            for axis2 in {0, 1, 2} - {axis1}:
                for sign2 in [1, -1]:
                    axis3 = 3 - (axis1 + axis2)
                    sign3 = 1 if (((axis2 - axis1) % 3 == 1) ^ (sign1 != sign2)) else -1
                    yield [Point(pos[axis1] * sign1, pos[axis2] * sign2, pos[axis3] * sign3) for pos in scanner]


def num_matches(points):
    # Find the best position for these points to align with the locked beacons
    # Done by finding the occurances of each diff from unknown -> known beacon
    diff_counts = {}
    diff_pos = {}
    for anchor in locked_beacons:
        for rel in points:
            d = diff(anchor, rel)
            if d not in diff_counts:
                diff_counts[d] = 0
                diff_pos[d] = Point(anchor.x - rel.x, anchor.y - rel.y, anchor.z - rel.z)
            diff_counts[d] += 1
    
    best_diff = max([d for d in diff_counts.keys()], key=lambda d: diff_counts[d])
    return diff_counts[best_diff], diff_pos[best_diff]


def try_match(scanner):
    # Try every possible orientation for this scanner
    for orientation in orientations(scanner):
        # Find the best position for this orientation (maximizes matches)
        matches, position = num_matches(orientation)
        if matches >= 12:
            # If there are at least 12 matching beacons, we've found the correct position
            locked_beacons.update([Point(position.x + p.x, position.y + p.y, position.z + p.z) for p in orientation])
            scanner_pos.append(position)
            return True

    # No good orientation/position found, return False
    return False


# Read in file
scanners = []
with open(sys.argv[1]) as infile:
    for line in infile:
        if line.startswith('---'):
            scanners.append([])
        elif len(line.strip()) > 0:
            scanners[-1].append(Point(*map(int, line.split(','))))

# We assume Scanner 0 is at (0, 0, 0) in the "true" orientation 
locked_beacons = set()
unknown_scanners = []
scanner_pos = []

locked_beacons.update(scanners[0])
unknown_scanners = scanners[1:]
scanner_pos.append(Point(0, 0, 0))

# Iterate until there are no unknown scanners
while len(unknown_scanners) > 0:
    for scanner in unknown_scanners:
        if try_match(scanner):
            unknown_scanners.remove(scanner)
            print(len(locked_beacons))

# Part 1: Total number of beacons
print(f"Part 1: Number of Beacons: {len(locked_beacons)}")

# Part 2: Max Manhattan distance between scanners
max_dist = max([manhattan(p1, p2) for p1 in scanner_pos for p2 in scanner_pos])
print(f"Part 2: Max Manhattan Distance: {max_dist}")