from collections import defaultdict

line = open("inputs/input_11.txt").readline()
stones = defaultdict(int)
for stone in line.strip().split():
    stones[stone] = 1

def permute(stones, blinks=25):
    for i in range(0, blinks):
        new_stones = defaultdict(int)
        for (key,value) in stones.items():
            if key == "0":
                new_stones["1"] += value
            elif len(key) % 2 == 0:
                left = int(key[:len(key)//2])
                right = int(key[len(key)//2:])

                new_stones[str(left)] += value
                new_stones[str(right)] += value
            else:
                new_stones[str(2024 * int(key))] += value
        stones = new_stones
    return stones

stones_1 = permute(stones)
numbers_of_stones = sum([value for value in stones_1.values()])
print("Part 1:", numbers_of_stones)

stones = permute(stones, 75)
numbers_of_stones = sum([value for value in stones.values()])
print("Part 2:", numbers_of_stones)