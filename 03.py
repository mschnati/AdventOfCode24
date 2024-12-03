i = "inputs/input_03.txt"
t = "test.txt"
with open(i) as file:
    memory = file.read()


def part_1(memory: str):
    result = 0
    while memory != "":
        memory = memory.partition('mul(',)[-1]
        partition = memory.partition(')')
        memory = partition[-1]
        param = partition[0]
        param_split = param.split(',')

        if len(param_split) != 2: # not 2 params
            memory = partition[0] + partition[1] + partition[-1] # rebuild string and check after previous 'mul('
            continue

        if param_split[0].isnumeric() and param_split[1].isnumeric():
            result += int(param_split[0]) * int(param_split[1])
        else:
            memory = partition[0] + partition[1] + partition[-1]

    return result

print('Part 1: ' + str(part_1(memory)))

