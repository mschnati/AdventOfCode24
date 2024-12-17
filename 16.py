import heapq

inp = "inputs/input_16.txt"
test = "test.txt"

grid = []
with open(inp) as file:
    for i, line in enumerate(file):
        grid.append([])
        for j, char in enumerate(line.strip()):
            grid[i].append(char)
            if char == 'S':
                start = (i, j)
            if char == 'E':
                end = (i, j)

# print grid as list comprehension
print('\n'.join([''.join(row) for row in grid]))

facing = (0, 1) # (y, x), east

def print_path(path):
    grid_copy = [row.copy() for row in grid]
    for y, x in path:
        grid_copy[y][x] = 'O'
    print('\n'.join([''.join(row) for row in grid_copy]))

# move: cost 1, turn 90 degrees: cost 1000, turn and move: cost 1001
# '#' = wall, '.' = open, 'S' = start, 'E' = end

def part_2(grid, start, facing, end):
    min_cost = {}
    min_end_cost = float('inf')
    predecessors = {}
    heap = []
    heapq.heappush(heap, (0, start, facing))
    
    while heap:
        cost, pos, facing = heapq.heappop(heap)
        key = (pos, facing)
        
        # Prune paths exceeding minimal end cost
        if cost > min_end_cost:
            continue

        if key in min_cost and cost > min_cost[key]:
            continue
        min_cost[key] = cost
        
        # If we reach the end, update the minimal end cost
        if pos == end:
            if cost < min_end_cost:
                min_end_cost = cost
            # Continue to find all paths with minimal cost
            continue

        # Explore neighboring positions
        for dy, dx in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            new_facing = (dy, dx)
            new_pos = (pos[0] + dy, pos[1] + dx)
            if not (0 <= new_pos[0] < len(grid)) or not (0 <= new_pos[1] < len(grid[0])):
                continue  # Out of bounds
            if grid[new_pos[0]][new_pos[1]] == '#':
                continue  # Wall

            move_cost = 1 if new_facing == facing else 1001
            new_cost = cost + move_cost
            new_key = (new_pos, new_facing)
            
            # Prune paths exceeding minimal end cost
            if new_cost > min_end_cost:
                continue

            # Update min_cost and predecessors
            if new_key not in min_cost or new_cost < min_cost[new_key]:
                min_cost[new_key] = new_cost
                predecessors[new_key] = [key]
                heapq.heappush(heap, (new_cost, new_pos, new_facing))
            elif new_cost == min_cost[new_key]:
                predecessors[new_key].append(key)
                heapq.heappush(heap, (new_cost, new_pos, new_facing))  # Continue exploring

    # Collect all positions on shortest paths
    end_keys = [key for key in min_cost if key[0] == end and min_cost[key] == min_end_cost]
    positions_on_shortest_paths = set()
    visited_keys = set()
    stack = end_keys.copy()

    while stack:
        key = stack.pop()
        if key in visited_keys:
            continue
        visited_keys.add(key)
        pos, facing = key
        positions_on_shortest_paths.add(pos)
        if key in predecessors:
            for prev_key in predecessors[key]:
                stack.append(prev_key)
    
    # Return the number of unique tiles visited and the positions and the cost
    return len(positions_on_shortest_paths), positions_on_shortest_paths, min_end_cost

visited_tiles_count, positions, cost = part_2(grid, start, facing, end)
print_path(positions)#
print("Part 1:", cost)
print("Part 2:", visited_tiles_count)

