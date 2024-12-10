i = "inputs/input_09.txt"
t = "test.txt"
with open(i) as file:
    disk_map = file.read().strip()

def is_even(num):
    return num % 2 == 0

def convert(disk_map):
    output = []
    id_num = 0
    for i, digit in enumerate(disk_map):
        digit = int(digit)
        if is_even(i):
            for _ in range(digit):
                output.append(id_num)
            id_num += 1
        else:
            for _ in range(digit):
                output.append('.')
    
    return output

'''
move file blocks one at a time from the end of the disk to the leftmost free space block 
(until there are no gaps remaining between file blocks). For the disk map 12345, the process looks like this:

0..111....22222
02.111....2222.
022111....222..
0221112...22...
02211122..2....
022111222......
'''
def move_files(file_system):
    front = 0
    end = len(file_system) - 1
    while front < end:
        while file_system[front] != '.':
            front += 1
        while file_system[end] == '.':
            end -= 1
        if end <= front:
            break
        file_system[front] = file_system[end]
        file_system[end] = '.'
        
    return file_system

def checksum(file_system):
    checksum = 0
    for i, digit in enumerate(file_system):
        if digit == '.':
            continue
        digit = int(digit)
        checksum += i * digit

    return checksum
converted = convert(disk_map)
part_1 = move_files(converted)
print("Part 1: " + str(checksum(part_1)))

'''--- Part Two ---
rather than move individual blocks, compact the files on his disk by moving whole files instead.
Attempt to move whole files to the leftmost span of free space blocks that could fit the file. 
Attempt to move each file exactly once in order of decreasing file ID number starting with the file with the highest file ID number. 
If there is no span of free space to the left of a file that is large enough to fit the file, the file does not move.

The first example from above now proceeds differently:

00...111...2...333.44.5555.6666.777.888899
0099.111...2...333.44.5555.6666.777.8888..
0099.1117772...333.44.5555.6666.....8888..
0099.111777244.333....5555.6666.....8888..
00992111777.44.333....5555.6666.....8888..

The process of updating the filesystem checksum is the same; now, this example's checksum would be 2858.
Using this new method instead. What is the resulting filesystem checksum?
'''
#find blocks of '.'. save how long they are and where they start
def find_gaps(file_system):
    gaps = []
    gap = 0
    for i, digit in enumerate(file_system):
        if digit == '.':
            gap += 1
        else:
            if gap > 0:
                gaps.append((i - gap, gap))
                gap = 0
    return gaps

# from right to left, try to fit blocks of the same number into the leftmost gap that can fit it
def move_files_2(file_system, gaps):
    # switched ids dict
    switched = {}
    i = len(file_system) - 1
    while i > 0:
        found = False
        if file_system[i] == '.':
            i -= 1
            continue
        id_num = file_system[i]
        if id_num in switched:
            i -= 1
            continue
        size = 1
        while file_system[i - size] == id_num:
            size += 1
        for j, gap in enumerate(gaps):
            if gap[0] > i:
                break
            if gap[1] >= size:
                found = True
                # save the id number that was switched
                switched[id_num] = True
                for k in range(size):
                    file_system[gap[0] + k] = id_num
                gaps[j] = (gap[0] + size, gap[1] - size)
                # remove gap if it's been filled
                if gaps[j][1] == 0:
                    gaps.pop(j)
                break
            
        # write '.' where the file was
        if found:
            for k in range(size):
                file_system[i - k] = '.'

        i -= size
    return file_system

converted = convert(disk_map)
gaps = find_gaps(converted)
part_2 = move_files_2(converted, gaps)
print("Part 2: " + str(checksum(part_2)))
