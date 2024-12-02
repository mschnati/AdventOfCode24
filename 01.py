list_1 = []
list_2 = []
with open("inputs/input_01.txt") as file:
    for line in file:
        if line.strip():
            num1, num2 = map(int, line.split())
            list_1.append(num1)
            list_2.append(num2)

list_1.sort()
list_2.sort()
result_1 = 0
for i, num in enumerate(list_1):
    if num > list_2[i]:
        result_1 += num - list_2[i]
    else:
        result_1 += list_2[i] - num

print("result 1: " + str(result_1))

result_2 = 0
j = 0
for i, num in enumerate(list_1):
    mult = 0
    while num >= list_2[j]:
        # print(str(num) + ' ' + str(list_2[j]))
        if num == list_2[j]:
            # print('found')
            mult += 1
        j += 1
    result_2 += num * mult

print("result 2: " + str(result_2))