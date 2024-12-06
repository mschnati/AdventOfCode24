i = "inputs/input_05.txt"
t = "test.txt"

rules = []
orders = []
with open(i) as file:
    for line in file:
        line = line.replace('\n', '')
        partition = line.partition('|')
        if partition[1] != '':
            rules.append((partition[0], partition[2]))
        else:
            orders.append(line.split(','))


def part_1(rules, orders):
    total = 0
    for order in orders:
        pages = [page.strip() for page in order if page.strip()] # remove empty strings
        if not pages:
            continue  # Skip empty orders
        pages_set = set(pages) # remove duplicates
        applicable_rules = [ # only keep rules that apply to both pages of the order
            (x.strip(), y.strip()) for x, y in rules
            if x.strip() in pages_set and y.strip() in pages_set
        ]

        index_map = {page: idx for idx, page in enumerate(pages)} # map page to index (75,47,61,53,29) -> {75: 0, 47: 1, 61: 2, 53: 3, 29: 4}

        valid = True
        for x, y in applicable_rules:
            if index_map[x] >= index_map[y]: # if the order of the pages != order in the rules
                valid = False
                break
        if valid:
            middle_index = len(pages) // 2 # integer division
            middle_page = int(pages[middle_index])
            total += middle_page
    print(total)


part_1(rules, orders)


'''--- Part Two ---
For each of the incorrectly-ordered updates, use the page ordering rules to put the page numbers in the right order. 
For the above example, here are the three incorrectly-ordered updates and their correct orderings:

    75,97,47,61,53 becomes 97,75,47,61,53.
    61,13,29 becomes 61,29,13.
    97,13,75,29,47 becomes 97,75,47,29,13.

Take only the incorrectly-ordered updates and order them correctly, their middle page numbers are 47, 29, and 47. Adding these together produces 123.

Find updates which are not in the correct order. Add up the middle page numbers after correctly ordering just those updates
'''
def part_2(rules, orders):
    total = 0
    for order in orders:
        pages = [page.strip() for page in order if page.strip()] # remove empty strings
        if not pages:
            continue  # Skip empty orders
        pages_set = set(pages) # remove duplicates
        applicable_rules = [ # only keep rules that apply to both pages of the order
            (x.strip(), y.strip()) for x, y in rules
            if x.strip() in pages_set and y.strip() in pages_set
        ]

        index_map = {page: idx for idx, page in enumerate(pages)} # map page to index (75,47,61,53,29) -> {75: 0, 47: 1, 61: 2, 53: 3, 29: 4}

        fixed = False
        valid = False
        while fixed is False: # until nothing had to be fixed
            fixed = True
            for x, y in applicable_rules:
                if index_map[x] >= index_map[y]: # fix pages if incorrectly ordered
                    index_map = {y if k == x else x if k == y else k: v for k, v in index_map.items()} 
                    fixed = False
                    valid = True
                    break
                    
        if valid:
            middle_index = len(pages) // 2 # integer division
            middle_page = int(list(index_map.keys())[list(index_map.values()).index(middle_index)]) # get key by value
            total += middle_page
    print(total)

part_2(rules, orders)