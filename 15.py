i = "inputs/input_15.txt"
t = "test.txt"

grid, moves = open(i).read().split('\n\n')

def move(p, d):
    p = (p[0] + d[0], p[1] + d[1])
    if all([
        grid[p] != '[' or move((p[0] + 1, p[1]), d) and move(p, d),
        grid[p] != ']' or move((p[0] - 1, p[1]), d) and move(p, d),
        grid[p] != 'O' or move(p, d), grid[p] != '#']):
            grid[p], grid[(p[0] - d[0], p[1] - d[1])] = grid[(p[0] - d[0], p[1] - d[1])], grid[p]
            return True

part = 0
for grid in grid, grid.translate(str.maketrans(
        {'#':'##', '.':'..', 'O':'[]', '@':'@.'})):
    
    # Convert the grid to a dictionary with (x, y) tuples as keys
    grid = {(i, j): c for j, r in enumerate(grid.split())
                     for i, c in enumerate(r)}

    pos, = [p for p in grid if grid[p] == '@']

    # Execute the moves
    for m in moves.replace('\n', ''):
        dir = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1)}[m]
        C = grid.copy()

        # Move the robot and revert if invalid
        if move(pos, dir): pos = (pos[0] + dir[0], pos[1] + dir[1])
        else: grid = C

    ans = sum(p[0] + p[1] * 100 for p in grid if grid[p] in 'O[')
    part += 1
    print("Part " + str(part) + ':', ans)

