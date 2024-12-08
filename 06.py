grid = []
startpos = ()
with open("inputs/input_06.txt") as file:
    for line in file:
        col = []
        for x in line.strip():
            if x == "^":
                startpos = (line.index(x), len(grid))
            col.append(x)
        grid.append(col)


dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def check_loop(new_grid):
    visited = set()
    k = 0
    new_X = startpos[0] + dirs[k][0]
    new_Y = startpos[1] + dirs[k][1]
    while True:
        if new_grid[new_Y][new_X] == "#":
            new_X -= dirs[k][0]
            new_Y -= dirs[k][1]

            k = (k + 1) % 4

        if (new_X, new_Y, k) in visited:
            return True, visited
    
        visited.add((new_X, new_Y, k))

        new_X += dirs[k][0]
        new_Y += dirs[k][1]

        if not (0 <= new_Y < len(grid)) or not (0 <= new_X < len(grid[0])):
            return False, visited

loop_counted = 0
_, guard_visited = check_loop(grid)

# remove direction value and then remove duplicates from guard_visited
guard_visited = [(x, y) for x, y, _ in guard_visited]
guard_visited = list(set(guard_visited))
print("Part 1: " + str(len(guard_visited)))

# only check cells visited by the guard
for (x, y) in guard_visited:
    grid[y][x] = "#"
    res, _ = check_loop(grid)
    if res:
        loop_counted += 1
    grid[y][x] = "."

print("Part 2: " + str(loop_counted))     