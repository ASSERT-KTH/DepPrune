import sys
import os
project = sys.argv[1]
basement = sys.argv[2]

def extract_substring(input_string):
    for index, char in enumerate(input_string):
        if char.isalpha() or char == "@":
            return input_string[index:]

def replace_str(input_string):
    last_at_index = input_string.rfind("@")

    if last_at_index != -1:
        part1 = input_string[:last_at_index]
        part2 = input_string[last_at_index+1:]
        
        modified_string = part1 + "__" + part2
        return modified_string



input_file_path = f"./{basement}/{project}/original_npm_list_filtered.txt"
output_array = []

with open(input_file_path, "r") as file:
    for line in file:
        output_array.append(line.strip())

output_array = output_array[1:-1]
# Extract substrings starting from the first alphabet or "@"
original_strings = []
for item in output_array:
    if "UNMET" not in item:
        substring = extract_substring(item)
        if substring:
            original_strings.append(substring)

result_strings = []
for item in original_strings:
    result_strings.append(replace_str(item))

print(project + "," + str(len(result_strings)))


total_deps_file = open(f'./{basement}/{project}/total_deps.txt', "a")
for item in result_strings:
    total_deps_file.writelines(item+ "\n")


total_deps_name = []
for item in result_strings:
    dep = item.split("__")
    name = dep[0]
    if name not in total_deps_name:
        total_deps_name.append(name)

total_deps_name_file = open(f'./{basement}/{project}/total_deps_name.txt', "a")
for item in total_deps_name:
    total_deps_name_file.writelines(item+ "\n")
