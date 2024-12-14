import math

i = "inputs/input_13.txt"
t = "test.txt"

machines = []
# [(x, y),(x, y),(x, y)]
with open(i) as file:
    for line in file:
        partition = line.strip().partition(':')
        if partition[1] == '':
            continue
        coordinates = partition[-1].partition(',')
        # Button A/B: X+94, Y+34
        if partition[0][-1] == 'A' or partition[0][-1] == 'B':
            x = coordinates[0].partition('+')[-1]
            y = coordinates[-1].partition('+')[-1]
            if partition[0][-1] == 'A':
                machines.append([(int(x), int(y))])
            else: 
                machines[-1].append((int(x), int(y)))
        else:
            # Prize: X=18641, Y=10279
            x = coordinates[0].partition('=')[-1]
            y = coordinates[-1].partition('=')[-1]
            machines[-1].append((int(x), int(y)))

# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400
# 94a + 22b = 8400
# 34a + 67b = 5400

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

def solve_equation(button_a, button_b, prize):
    lcm_a = lcm(button_a[0], button_a[1])
    mult_1 = lcm_a // button_a[0]
    mult_2 = -(lcm_a // button_a[1])
    eq_1 = [button_a[0] * mult_1, button_b[0] * mult_1, prize[0] * mult_1]
    eq_2 = [button_a[1] * mult_2, button_b[1] * mult_2, prize[1] * mult_2]

    # add eq_1 and eq_2
    div = eq_1[1] + eq_2[1]
    b = eq_1[2] + eq_2[2]
    # solve for b
    b = b / div
    # substitute b into eq_1
    a = (prize[0] - button_b[0] * b) / button_a[0]
    return a, b

def part_1(machines):
    tokens = 0
    for machine in machines:
        a, b = solve_equation(machine[0], machine[1], machine[2])
        if a % 1 == 0 and b % 1 == 0: # only integer solution are valid
            tokens += int(a*3 + b)

    return tokens

print("Part 1:" , part_1(machines))

# Part 2
# add 10000000000000 to every prize

def part_2(machines):
    tokens = 0
    for machine in machines:
        a, b = solve_equation(machine[0], machine[1], (machine[2][0] + 10000000000000, machine[2][1] + 10000000000000))
        if a % 1 == 0 and b % 1 == 0: # only integer solution are valid
            tokens += int(a*3 + b)

    return tokens

print("Part 2:" , part_2(machines))