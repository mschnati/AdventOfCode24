i = "inputs/input_03.txt"
t = "test.txt"
with open(i) as file:
    memory = file.read()

'''
mul(X,Y), where X and Y are each 1-3 digit numbers. For instance, mul(44,46) multiplies 44 by 46 to get a result of 2024. Similarly, 
mul(123,4) would multiply 123 by 4.

Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.

xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))

Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

Scan the corrupted memory for uncorrupted mul instructions. Add up all of the results of the multiplications
'''

def eval_next_mult(memory: str):
    memory = memory.partition('mul(')[-1]
    partition = memory.partition(')')
    memory = partition[-1]
    param = partition[0]
    param_split = param.split(',')

    if len(param_split) != 2: # not 2 params
        memory = partition[0] + partition[1] + partition[-1] # rebuild string and check after previous 'mul('
        return memory, 0

    if param_split[0].isnumeric() and param_split[1].isnumeric():
        result = int(param_split[0]) * int(param_split[1])
        return memory, result
    else:
        memory = partition[0] + partition[1] + partition[-1]
    return memory, 0

def part_1(memory: str):
    result = 0
    while memory != "":
        memory, add = eval_next_mult(memory)
        result += add

    return result

print('Part 1: ' + str(part_1(memory)))

'''--- Part Two ---
There are two new instructions you'll need to handle:

    The do() instruction enables future mul instructions.
    The don't() instruction disables future mul instructions.

Only the most recent do() or don't() instruction applies. At the beginning of the program, mul instructions are enabled.

For example:

xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))

This time, the sum of the results is 48 (2*4 + 8*5).

add up all of the results of just the enabled multiplications
'''

def part_2(memory: str):
    result = 0

    while memory != "":
        while (memory != ""):
            pre_mul = memory.partition('mul(')[0]
            dont = pre_mul.find('don\'t()') # dont in part before 'mul('
            if dont == -1:
                memory, add = eval_next_mult(memory)
                result += add
            else:
                break

        memory = memory.partition('do()')[-1]

    return result

print("Part 2: " + str(part_2(memory)))
