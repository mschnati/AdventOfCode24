i = 'inputs/input_07.txt'
t = 'test.txt'
calculations = []
with open(i) as file:
    for line in file:
        calculations.append(line.strip())

def test_calc_1(value, numbers):
    if len(numbers) == 1:
        return numbers[0] == value
    
    mult = False
    add = False

    # check for multiplication only if the number divides the value
    if numbers[-1] != 0 and value % numbers[-1] == 0:
        mult = test_calc_1(value // numbers[-1], numbers[:-1])

    add = test_calc_1(value - numbers[-1], numbers[:-1])

    return mult or add


'''
Process each equation and determine which one can be solved using '*' and '+' while always evaluation left to right
Add up the values of all solvable equations

Solution: go from right to left to only have to test viable solutions
'''
def part_1(calculations):
    result = 0
    for calc in calculations:
        parts = calc.partition(':')
        test_value = int(parts[0])
        numbers = [int(x) for x in parts[-1].strip().split(' ')]

        if test_calc_1(test_value, numbers):
            result += test_value

    return result

print(f"Part 1: {part_1(calculations)}")


def test_calc_2(value, numbers):
    if len(numbers) == 1:
        return numbers[0] == value
    
    mult = False
    add = False
    concat = False

    # check for multiplication only if the number divides the value
    if numbers[-1] != 0 and value % numbers[-1] == 0:
        mult = test_calc_2(value // numbers[-1], numbers[:-1])
    
    # check for concatenation only if the values last digits match the numbe
    num_digits = (10 ** len(str(numbers[-1])))
    digits = value % num_digits
    if digits == numbers[-1]:
        concat = test_calc_2(value // num_digits, numbers[:-1])

    add = test_calc_2(value - numbers[-1], numbers[:-1])

    return mult or add or concat

'''
Same with added concatenation operator '||'
'''
def part_2(calculations):
    result = 0
    for calc in calculations:
        parts = calc.partition(':')
        test_value = int(parts[0])
        numbers = [int(x) for x in parts[-1].strip().split(' ')]

        if test_calc_2(test_value, numbers):
            result += test_value

    return result

print(f"Part 2: {part_2(calculations)}")