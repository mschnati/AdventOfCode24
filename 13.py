
i = "inputs/input_10.txt"
t = "test.txt"

machines = []
# [(x, y),(x, y),(x, y)]
with open(t) as file:
    for line in file:
        partition = line.strip().partition(':')
        print(partition[0])
        if partition[1] == '':
            continue
        coordinates = partition[-1].partition(',')
        # Button A/B: X+94, Y+34
        if partition[0][-1] == 'A' or partition[0][-1] == 'B':
            x = coordinates[0].partition('+')[-1]
            y = coordinates[-1].partition('+')[-1]
            if partition[0][-1] == 'A':
                machines.append([(x, y)])
            else: 
                machines[-1].append((x, y))
        else:
            # Prize: X=18641, Y=10279
            x = coordinates[0].partition('=')[-1]
            y = coordinates[-1].partition('=')[-1]
            machines[-1].append((x, y))

print(machines)

