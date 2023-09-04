import sys
import os
project = sys.argv[1]

def extract_substring(input_string):
    for index, char in enumerate(input_string):
        if char.isalpha() or char == "@":
            return input_string[index:]

input_file_path = f"./TestCollection/{project}/npm_list_filtered_output_debloated.txt"  # Replace with the path to your text file
output_array = []

# Read the file line by line and store lines in the array
with open(input_file_path, "r") as file:
    for line in file:
        output_array.append(line.strip())

# Remove the first and last items
output_array = output_array[1:-1]

# Extract substrings starting from the first alphabet or "@"
result_substrings = []
for item in output_array:
    if "UNMET" not in item:
        substring = extract_substring(item)
        if substring:
            result_substrings.append(substring)

total_deps_file = open(f'./Playground/{project}/total_deps_debloated.txt', "a")
for item in result_substrings:
    total_deps_file.writelines(item+ "\n")
print("Done")
