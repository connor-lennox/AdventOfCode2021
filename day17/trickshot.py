import sys


with open(sys.argv[1]) as infile:
    input = infile.__next__().split('=')

x_range = tuple(int(i) for i in input[1].split(',')[0].split('..'))
y_range = tuple(int(i) for i in input[2].split('..'))

max_y_vel = abs(min(y_range))

print(f"Part 1: Max Height: {sum(range(1, max_y_vel))}")


def simulate(vx, vy):
    x, y = 0, 0
    vxx, vyy = vx, vy
    while x <= max(x_range) and y >= min(y_range):
        x += vxx
        y += vyy
        if vxx > 0: vxx -= 1
        vyy -= 1
        if min(x_range) <= x <= max(x_range) and min(y_range) <= y <= max(y_range):
            return True
    return False


num_settings = sum([
    simulate(vx, vy)
    for vx in range(0, max(x_range)+1)
    for vy in range(-max_y_vel, max_y_vel)
])

print(f"Part 2: Num Valid Settings: {num_settings}")
