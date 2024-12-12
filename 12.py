from collections import defaultdict
i = "inputs/input_12.txt"
t = "test.txt"

grid = []
regions = []
visited = set()
with open(i) as file:
    for y, line in enumerate(file):
        grid.append([])
        for x, char in enumerate(line.strip()):
            grid[y].append(char)

def in_bounds(y, x):
    return (0 <= y < len(grid)) and (0 <= x < len(grid[0]))

dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def map_region(y, x, region):
    if (y, x) in visited:
        return
    visited.add((y, x))
    regions[-1].append((y, x))
    regions[-1][0] += 1
    for dy, dx in dirs:
        ny, nx = y + dy, x + dx
        if not in_bounds(ny, nx) or grid[ny][nx] != region:
            regions[-1][1] += 1
        else:
            map_region(ny, nx, region)

for y in range(len(grid)):
    for x in range(len(grid[0])):
        if (y, x) not in visited:
            regions.append(list())
            regions[-1].append(0) # area counter
            regions[-1].append(0) # perimeter counter
            map_region(y, x, grid[y][x])

total = 0
for region in regions:
    total += region[0] * region[1]

print("Part 1:" ,total)

coner_dirs = [(0.5, 0.5), (-0.5, 0.5), (0.5, -0.5), (-0.5, -0.5)]
        
def part_2():
    seen = set()
    # find all plant regions on the grid
    plant_map = []
    for y in range(0, len(grid)):
        for x in range(0, len(grid[0])): 
            moves = [(y, x)]

            if (y,x) in seen:
                continue
            plant = []        
            while len(moves) != 0:
                move = moves.pop()
                
                if (move[0], move[1]) in seen:
                    continue
                seen.add((move[0], move[1]))

                plant.append([move[0], move[1]])
                
                # up, down, left, right y x
                for dir in dirs:
                    n_y = move[0]+dir[0]
                    n_x = move[1]+dir[1]

                    if in_bounds(n_y, n_x):
                        if grid[n_y][n_x] == grid[move[0]][move[1]] and not ((n_y, n_x) in seen):
                            moves.append((n_y, n_x))
            
            if len(plant) != 0:
                plant_map.append(plant)


    price = 0    
    for plant in plant_map:
        # find all corners of every square of the plant
        corners = set()
        for (y, x) in plant:
            for dir in coner_dirs:
                corners.add((y+dir[0], x+dir[1]))

        corners_count = 0
        for (y, x) in corners:
            variants = []
            # check what type of corner it is. 
            # bottom right, top right, bottom left, top left
            for n_y, n_x in [(y - 0.5, x - 0.5), (y + 0.5, x - 0.5), (y + 0.5, x + 0.5), (y - 0.5, x + 0.5)]:
                variants.append([n_y, n_x] in plant)

            number = sum(variants) # number of plants around the corner
            if number == 1:
                corners_count += 1
            elif number == 2: # could be straight or corner
                # XX or  X        X
                #         X  or X
                if variants == [True, False, True, False] or variants == [False, True, False, True]: # corner
                    corners_count += 2
            elif number == 3:
                corners_count += 1
        price += len(plant) * corners_count
    return price

print("Part 2:", part_2())