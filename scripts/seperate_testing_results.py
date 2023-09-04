import sys
import json
import os

filePath = f'./temp_passed_output.txt'
# filePath = f"./test_indirect_nonisolated_output_total.txt"
with open(filePath) as f:
    lines = f.read().splitlines()

pck_dict = {}

for line in lines:
    result = line.split(",")
    pck_name = result[0]
    dep_name = result[1]

    if pck_name not in pck_dict:
        pck_dict[pck_name] = []
    pck_dict[pck_name].append(dep_name)

for key, value in pck_dict.items():
    # output_file = open(f'./Playground/{key}/nonisolated_deps_passed.txt', "a")
    output_file = open(f'./Playground/{key}/indirect_confirmed_deps.txt', "a")
    for item in value:
        output_file.writelines(item+"\n")
        
print("Done")