import sys
import os
project = sys.argv[1]

def count_duplicates(input_list):
    item_counts = {}
    for item in input_list:
        if item in item_counts:
            item_counts[item] += 1
        else:
            item_counts[item] = 1
    
    duplicated_count = sum(1 for count in item_counts.values() if count > 1)
    return duplicated_count

input_file_path = f"./Playground/{project}/total_deps.txt"  # Replace with the path to your text file
output_array = []

# Read the file line by line and store lines in the array
with open(input_file_path) as f:
    lines1 = f.read().splitlines()

# duplicated_count = count_duplicates(lines1)
# print(project + "," + str(duplicated_count))

dedup_lines1 = list(set(lines1))
print(project + "," + str(len(dedup_lines1)))