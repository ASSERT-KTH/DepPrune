import sys
import os
import json

project = sys.argv[1]

json_path = f'./Playground/{project}/coverage/coverage-final.json'
# json_path = f'./coverage-final.json'
coverage_file = open(json_path, encoding="utf-8")  
coverage_dict = json.load(coverage_file)
reachable_files = []
def is_list_all_zeros(lst):
    return all(x == 0 for x in lst)

def is_file_reachable(value):
    s_dict = value.get("s", {})
    s_all_zeros = all(value == 0 for value in s_dict.values())
    f_dict = value.get("f", {})
    f_all_zeros = all(value == 0 for value in f_dict.values())
    b_dict = value.get("b", {})
    b_all_zeros = all(is_list_all_zeros(value) for value in b_dict.values())

    if not s_all_zeros or not f_all_zeros or not b_all_zeros:
        return value.get("path")

for key, value in coverage_dict.items():
    # print(key)
    reachable = is_file_reachable(value)
    if reachable != None:
        reachable_files.append(reachable)

reachable_file_path = f'Playground/{project}/reachable_files_nyc.txt'
reachable_file = open(reachable_file_path, "a")
for item in reachable_files:
    reachable_file.writelines(item + '\n')

print(len(reachable_files))