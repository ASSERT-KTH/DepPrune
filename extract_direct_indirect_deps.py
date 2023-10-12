import sys
import os

project = sys.argv[1]

total_path = f'Playground/{project}/total_deps.txt'
with open(total_path) as f:
    total_deps = f.read().splitlines()

direct_path = f'Playground/{project}/direct_deps.txt'
with open(direct_path) as f:
    direct_deps = f.read().splitlines()

output_path = f'temp_log.txt'

def count_string_occurrences(string_array, target_string):
    count = 0 

    for element in string_array:
        if element == target_string:
            count += 1 

    return count

output_file = open(output_path, 'a')    
for dep in direct_deps:
    occurrences = count_string_occurrences(total_deps, dep)
    if occurrences > 1:
        output_file.writelines(f"{project},{dep},{occurrences}\n")