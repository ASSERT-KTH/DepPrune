import json
import sys

project = sys.argv[1]
file_path = f'Playground/{project}/original_npm_list_filtered.txt'

count = 0
with open(file_path, 'r') as file:
    for line in file:
        if "->" in line:
            count += 1
print(project + "," + str(count))