from collections import defaultdict
i = "inputs/input_15.txt"
t = "test.txt"

grid = []
start_pos = (0, 0)
moves = []
with open(i) as file:
    g = True
    for y, line in enumerate(file):
        if g:
            if line == "\n":
                g = False
                continue
            grid.append([])
            for x, char in enumerate(line.strip()):
                grid[y].append(char)
                if char == '@':
                    start_pos = (y, x)
        else:
            for char in line.strip():
                moves.append(char)

# print grid as list comprehension
# print('\n'.join([''.join(row) for row in grid]))

# up, down, left, right
dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_pushable(grid, box, direction):
    y, x = box
    if grid[y][x] == '.':
        grid[y][x] = 'O'
        return True
    if grid[y][x] == '#':
        return False
    n_y = y + direction[0]
    n_x = x + direction[1]
    return is_pushable(grid, (n_y, n_x), direction)

def push_box(grid, index, direction):
    y, x = index
    n_y = y + direction[0]
    n_x = x + direction[1]
    if is_pushable(grid, (n_y, n_x), direction):
        grid[y][x] = '@'
        return True
    return False

def part_1(grid):
    grid_1 = grid.copy()
    pos = start_pos
    for move in moves:
        match move:
            case '^':
                direction = dirs[0]
            case 'v':
                direction = dirs[1]
            case '<':
                direction = dirs[2]
            case '>':
                direction = dirs[3]
        y, x = pos
        n_y = y + direction[0]
        n_x = x + direction[1]

        if grid[n_y][n_x] == 'O':
            if push_box(grid_1, (n_y, n_x), direction):
                grid[y][x] = '.'
                pos = (n_y, n_x)
        elif grid[n_y][n_x] == '.':
            grid[y][x] = '.'
            grid[n_y][n_x] = '@'
            pos = (n_y, n_x)

        # print('\n'.join([''.join(row) for row in grid_1]))
        # print('\n')
    
    res = 0
    for y, row in enumerate(grid_1):
        for x, _ in enumerate(row):
            if grid[y][x] == 'O':
                res += 100 * y + x
    return res


print("Part 1:", part_1(grid))
