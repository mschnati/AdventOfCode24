from collections import defaultdict

i = "inputs/input_08.txt"
t = "test.txt"

grid = []
symbols = defaultdict(list)
with open(i) as file:
    for line in file:
        col = []
        for x in line.strip():
            if x != ".":
                symbols[x].append((line.index(x), len(grid)))
            col.append(x)
        grid.append(col)


def in_bounds(x, y):
    return (0 <= x < len(grid)) and (0 <= y < len(grid[0]))
'''
Calculate the distance between all of the same symbols and add/subtract it from both points
Count how many of those points are in bounds
'''
def part_1(symbols):
    antinodes = set()
    for value in symbols:
        for i, pos_1 in enumerate(symbols[value]):
            for pos_2 in symbols[value][i+1:]:
                # find distance
                dist_x = pos_2[0] - pos_1[0]
                dist_y = pos_2[1] - pos_1[1]
                new_pos_1_x = pos_1[0] - dist_x
                new_pos_1_y = pos_1[1] - dist_y
                if in_bounds(new_pos_1_x, new_pos_1_y):
                    antinodes.add((new_pos_1_x, new_pos_1_y))

                new_pos_2_x = pos_2[0] + dist_x
                new_pos_2_y = pos_2[1] + dist_y
                if in_bounds(new_pos_2_x, new_pos_2_y):
                    antinodes.add((new_pos_2_x, new_pos_2_y))

    return len(antinodes)

print(part_1(symbols))

''' --- Part Two ---
Keep adding the distance until out of bounds
'''
def part_2(symbols):
    antinodes = set()
    for value in symbols:
        for i, pos_1 in enumerate(symbols[value]):
            if len(symbols[value]) > 1:
                antinodes.add(pos_1) # add pos of tower

            # compare tower to all other ones
            for pos_2 in symbols[value][i+1:]:
                dist_x = pos_2[0] - pos_1[0]
                dist_y = pos_2[1] - pos_1[1]
                new_pos_1_x = pos_1[0] - dist_x
                new_pos_1_y = pos_1[1] - dist_y

                # keep adding distance until out of bounds
                while in_bounds(new_pos_1_x, new_pos_1_y):
                    antinodes.add((new_pos_1_x, new_pos_1_y))
                    new_pos_1_x = new_pos_1_x - dist_x
                    new_pos_1_y = new_pos_1_y - dist_y

                new_pos_2_x = pos_2[0] + dist_x
                new_pos_2_y = pos_2[1] + dist_y
                while in_bounds(new_pos_2_x, new_pos_2_y):
                    antinodes.add((new_pos_2_x, new_pos_2_y))
                    new_pos_2_x = new_pos_2_x + dist_x
                    new_pos_2_y = new_pos_2_y + dist_y

    return len(antinodes)

print(part_2(symbols))