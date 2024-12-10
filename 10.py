from collections import defaultdict


i = "inputs/input_10.txt"
t = "test.txt"

grid = []
trailheads = []

with open(i) as file:
    for i, line in enumerate(file):
        grid.append([])
        for j, char in enumerate(line.strip()):
            grid[i].append(char)
            if char == '0':
                trailheads.append((i, j)) # (y,x)

dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def in_bounds(y, x):
    return (0 <= y < len(grid)) and (0 <= x < len(grid[0]))

def find_trail(grid, trailhead, visited: set):
    count = 0
    y, x = trailhead
    step = int(grid[y][x])
    if step == 9:
        visited.add(trailhead)
        return 1
    for direction in dirs:
        new_x = x + direction[0]
        new_y = y + direction[1]
        
        if in_bounds(new_y, new_x):
            if int(grid[new_y][new_x]) == step +1:
                total = find_trail(grid, (new_y, new_x), visited)
                count += total

    return count

def part_1_2():
    count = 0 # total trails found
    unique = 0 # trails to unique peaks
    for trailhead in trailheads:
        visited = set()
        count += find_trail(grid, trailhead, visited)
        unique += len(visited)
    return count, unique

total, unique = part_1_2()

print("Part 1: " + str(unique) + ', ' + "Part 2: " + str(total))

