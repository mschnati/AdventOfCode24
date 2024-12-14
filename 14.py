from collections import defaultdict
import time

i = "inputs/input_14.txt"
t = "test.txt"

robots = []
# [(x, y),(x, y)]
with open(i) as file:
    for line in file:
        p, v = line.strip().split(' ')
        index = p.partition('=')[-1].split(',')
        velocity = v.partition('=')[-1].split(',')
        robots.append([index, velocity])

size_x = 101
size_y = 103

def move_robot(robot, moves):
    pos, vel = robot
    x, y = pos
    d_x, d_y = vel
    x = (int(x) + moves * int(d_x)) % size_x
    y = (int(y) + moves * int(d_y)) % size_y
    return x, y

# print map of positions. empy space is '.'
def print_map(positions):
    for y in range(size_y):
        for x in range(size_x):
            if (x, y) in positions:
                print(positions[(x, y)], end='')
            else:
                print('.', end='')
        print()


quad_x, quad_y = size_x // 2, size_y // 2

# count the number of robots in each quadrant. removing the robots that are in the middle
def count_quadrants(positions):
    quad_count = [0, 0, 0, 0]
    for position in positions:
        x, y = position
        if x < quad_x and y < quad_y:
            quad_count[0] += positions[position]
        elif x > quad_x and y < quad_y:
            quad_count[1] += positions[position]
        elif x < quad_x and y > quad_y:
            quad_count[2] += positions[position]
        elif x > quad_x and y > quad_y:
            quad_count[3] += positions[position]
    return quad_count



def part_1():
    positions = defaultdict(int)
    num_moves = 100
    for robot in robots:
        x, y = move_robot(robot, num_moves)
        positions[(x, y)] += 1
    quads = count_quadrants(positions)
    res = quads[0] * quads[1] * quads[2] * quads[3]
    return res


print("Part 1:", part_1())

def part_2():
    num_moves = 12
    while True:
        inp = input()
        if inp == 'q':
            break
        if inp == 'z':
            num_moves -= 103
        else:
            num_moves += 103
        positions = defaultdict(int)
        for robot in robots:
            x, y = move_robot(robot, num_moves)
            positions[(x, y)] += 1
        # clear screen
        print("\033[H\033[J")
        print_map(positions)
        print("Moves:", num_moves)
        # sleep
        time.sleep(0.15)

part_2()
