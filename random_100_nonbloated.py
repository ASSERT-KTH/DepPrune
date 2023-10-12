import random
import os

filePath1 = f'all_non_bloatet.txt'
with open(filePath1) as f:
    lines1 = f.read().splitlines()

filePath2 = f'direct_non_bloatet.txt'
with open(filePath2) as f:
    direct = f.read().splitlines()

indirect = list(set(lines1)-set(direct))

random_items = random.sample(direct, 10)
random_indirect_items = random.sample(indirect, 90)
random_items.extend(random_indirect_items)

output_path = f'random_100_nonbloated.txt'
output_file = open(output_path, "a")
for item in random_items:
    # print(item)
    output_file.writelines(item + '\n')