import copy
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

# up, down, left, right
dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_pushable(grid_copy, box, direction):
    y, x = box
    if grid_copy[y][x] == '.':
        grid_copy[y][x] = 'O'
        return True
    if grid_copy[y][x] == '#':
        return False
    n_y = y + direction[0]
    n_x = x + direction[1]
    return is_pushable(grid_copy, (n_y, n_x), direction)

def push_box(grid_copy, index, direction):
    y, x = index
    n_y = y + direction[0]
    n_x = x + direction[1]
    if is_pushable(grid_copy, (n_y, n_x), direction):
        grid_copy[y][x] = '@'
        return True
    return False

def calc_score(grid_copy):
    res = 0
    for y, row in enumerate(grid_copy):
        for x, char in enumerate(row):
            if char == 'O':
                res += 100 * y + x
    return res

def part_1():
    grid_copy = copy.deepcopy(grid)
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

        if grid_copy[n_y][n_x] == 'O':
            if push_box(grid_copy, (n_y, n_x), direction):
                grid_copy[y][x] = '.'
                pos = (n_y, n_x)
        elif grid_copy[n_y][n_x] == '.':
            grid_copy[y][x] = '.'
            grid_copy[n_y][n_x] = '@'
            pos = (n_y, n_x)

        # print('\n'.join([''.join(row) for row in grid_1]))
        # print('\n')
    
    res = calc_score(grid_copy)
    return res

print("Part 1:", part_1())

def is_pushable_2(grid_copy, left, right, direction):
    y_l, x_l = left
    y_r, x_r = right
    if grid_copy[y_l][x_l] == '.' and grid_copy[y_r][x_r] == '.':
        return True
    if grid_copy[y_l][x_l] == '#' or grid_copy[y_r][x_r] == '#':
        return False
    n_y_l = y_l + direction
    n_y_r = y_r + direction
    # recursively check if there are more boxes to the left or right
    pushable = True
    if grid_copy[n_y_l][x_l] == ']':
        left = (n_y_l, x_l - 1)
        right = (n_y_l, x_l)
        if not is_pushable_2(grid_copy, left, right, direction):
            pushable = False
    if grid_copy[n_y_r][x_r] == '[':
        left = (n_y_r, x_r)
        right = (n_y_r, x_r + 1)
        if not is_pushable_2(grid_copy, left, right, direction):
            pushable = False
    if not pushable:
        return False
    return is_pushable_2(grid_copy, (n_y_l, x_l), (n_y_r, x_r), direction)

def push_sideways(grid_copy, box, direction):
    y, x = box
    if grid_copy[y][x] == '.':
        # move back to where we came from
        n_x = x - direction
        while grid_copy[y][n_x] != '@':
            n_x = x - direction
            grid_copy[y][x] = grid_copy[y][n_x]
            x = n_x
        grid_copy[y][x] = '.'
        return True
    if grid_copy[y][x] == '#':
        return False
    n_x = x + direction
    return push_sideways(grid_copy, (y, n_x), direction)

def push_wide(grid_copy, left, right, direction):
    # this will only be called if the boxes are pushable and only up or down
    y_l, x_l = left
    y_r, x_r = right
    if grid_copy[y_l][x_l] == '[': # grid_copy[y_r][x_r] == ']' implied
        # only one box in the way
        push_wide(grid_copy, (y_l + direction, x_l), (y_r + direction, x_r), direction)
    elif grid_copy[y_l][x_l] == ']':
        push_wide(grid_copy, (y_l + direction, x_l - 1), (y_l + direction, x_l), direction)
    if grid_copy[y_r][x_r] == '[':
        push_wide(grid_copy, (y_r + direction, x_r), (y_r + direction, x_r + 1), direction)
    if grid_copy[y_l - direction][x_l] == '@' or grid_copy[y_r - direction][x_r] == '@':
        return
    grid_copy[y_l][x_l] = grid_copy[y_l - direction][x_l]
    grid_copy[y_r][x_r] = grid_copy[y_r - direction][x_r]
    grid_copy[y_l - direction][x_l] = '.'
    grid_copy[y_r - direction][x_r] = '.'

def score_2(grid_copy):
    res = 0
    for y, row in enumerate(grid_copy):
        for x, char in enumerate(row):
            if char == '[':
                res += 100 * y + x
    return res

def part_2(grid):
    wide_grid = []
    for y, row in enumerate(grid):
        wide_grid.append([])
        for x, char in enumerate(row):
            match char:
                case '#' | '.':
                    wide_grid[y].append(char)
                    wide_grid[y].append(char)
                case 'O':
                    wide_grid[y].append('[')
                    wide_grid[y].append(']')
                case '@':
                    wide_grid[y].append(char)
                    pos = (y, wide_grid[y].index(char))
                    wide_grid[y].append('.')

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

        if wide_grid[n_y][n_x] == '[': 
            if move == '^' or move == 'v':
                if is_pushable_2(wide_grid, (n_y, n_x), (n_y, n_x+1), direction[0]):
                    push_wide(wide_grid, (n_y, n_x), (n_y, n_x+1), direction[0])
                    wide_grid[y][x] = '.'
                    wide_grid[n_y][n_x] = '@'
                    pos = (n_y, n_x)
            else:
                if push_sideways(wide_grid, (n_y, n_x), direction[1]):
                    pos = (n_y, n_x)
        elif wide_grid[n_y][n_x] == ']': 
            if move == '^' or move == 'v':
                if is_pushable_2(wide_grid, (n_y, n_x-1), (n_y, n_x), direction[0]):
                    push_wide(wide_grid, (n_y, n_x-1), (n_y, n_x), direction[0])
                    wide_grid[y][x] = '.'
                    wide_grid[n_y][n_x] = '@'
                    pos = (n_y, n_x)
            else:
                if push_sideways(wide_grid, (n_y, n_x), direction[1]):
                    pos = (n_y, n_x)
        elif wide_grid[n_y][n_x] == '.':
            wide_grid[y][x] = '.'
            wide_grid[n_y][n_x] = '@'
            pos = (n_y, n_x)

    print('\n'.join([''.join(row) for row in wide_grid]))
    print('\n')
    res = score_2(wide_grid)
    return res

    
print("Part 2:",part_2(grid))
