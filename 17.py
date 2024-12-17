inp = "inputs/input_17.txt"
test = "test.txt"

with open(inp) as file:
    for line in file:
        part = line.partition(':')
        if part[0][-1] == 'A':
            A = int(part[-1].strip())
        elif part[0][-1] == 'B':
            B = int(part[-1].strip())
        elif part[0][-1] == 'C':
            C = int(part[-1].strip())
        elif part[1] == ':':
            program = part[-1].strip().split(',')

program = [int(x) for x in program]
print(A,B,C)
print(program)

def combo(operand):
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4:
            return A
        case 5:
            return B
        case 6:
            return C
        case _:
            print('Invalid operand:', operand)
            return None

pc = 0
while pc < len(program):
    opcode = program[pc]
    match opcode:
        case 0: # adv
            A = A // 2 ** combo(program[pc + 1])
        case 1: # bxl
            B = B & program[pc + 1]
        case 2: # bst 
            B = combo(program[pc + 1]) % 8
        case 3: # jnz
            if A != 0:
                pc = program[pc + 1]
                continue
        case 4: # bxc
            B = B & C
        case 5: # out
            print(str(combo(program[pc + 1]) % 8) + ',', end='')
        case 6: # bdv
            B = A // 2 ** combo(program[pc + 1])
        case 7: # cdv
            C = A // 2 ** combo(program[pc + 1])
    pc += 2
print()
print("A:", A, "B:", B, "C:", C)