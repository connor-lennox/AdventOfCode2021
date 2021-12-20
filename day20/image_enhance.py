import sys


def map_line(line):
    return [1 if c == '#' else 0 for c in line.strip()]


with open(sys.argv[1]) as infile:
    algo = map_line(infile.readline())
    image_lines = [map_line(line) for line in infile if line.strip()]


# Part 1: Two convolution operations
def enhance(iterations):
    # Make a "working image" that is padded by each direction per iteration)
    pad = iterations
    working_height = len(image_lines) + pad * 2
    working_width = len(image_lines[0]) + pad * 2
    image = []

    # Top padded rows
    image.extend([[0 for _ in range(working_width)]] * pad)
    # Copy image with padded sides
    for line in image_lines:
        image.append([0] * pad)
        image[-1].extend(line)
        image[-1].extend([0] * pad)
    # Bottom padded rows
    image.extend([[0 for _ in range(working_width)]] * pad)

    # Keep track of the value of the "outer boundary"
    boundary_value = 0

    # Functions to fetch values from grid (incorporating boundary) and convolution
    def get_value(x, y):
        if x >= 0 and x < working_width and y >= 0 and y < working_height:
            return image[y][x]
        else:
            return boundary_value

    def convolve(x, y):
        idx = "".join([str(get_value(x+dx, y+dy)) for dy in range(-1, 2) for dx in range(-1, 2)])
        return algo[int(idx, 2)]


    # Perform the convolution
    for _ in range(iterations):
        image = [[convolve(x, y) for x in range(working_width)] for y in range(working_height)]
        boundary_value = algo[0] if boundary_value == 0 else algo[-1]

    return image


# Actually run enhance
p1_image = enhance(2)
print(f"Part 1: Total Lit Pixels: {sum([sum(line) for line in p1_image])}")
p2_image = enhance(50)
print(f"Part 2: Total Lit Pixels: {sum([sum(line) for line in p2_image])}")
