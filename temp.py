import sys
import os
project = sys.argv[1]

# def extract_substring(input_string):
#     for index, char in enumerate(input_string):
#         if char.isalpha() or char == "@":
#             return input_string[index:]

# def replace_str(input_string):
#     last_at_index = input_string.rfind("@")

#     if last_at_index != -1:
#         part1 = input_string[:last_at_index]
#         part2 = input_string[last_at_index+1:]
        
#         modified_string = part1 + "__" + part2
#         return modified_string

# file_path = f'../CJS-Debloator/Playground/{project}/npm_list_output.txt'
# with open(file_path) as f:
#     dep_tree = f.read().splitlines()
#     count = len(dep_tree) - 1

# bloated_path = f'./Playground/{project}/opened_bloated_deps_version.txt'
# with open(bloated_path) as f:
#     bloated_deps = f.read().splitlines()

# count = 0
# for item in dep_tree:
#     substring = extract_substring(item)
#     if substring:
#         cur_dep = replace_str(substring)
#         if cur_dep in bloated_deps:
#             count = count + 1

# print(f'{project},{count}')

filePath1 = f'./Playground/{project}/direct_offspring_removed.txt'
lines_len = 0
if os.path.exists(filePath1):
    with open(filePath1) as f:
        lines1 = f.read().splitlines()
    lines_len = len(lines1)

# filePath2 = f'./Playground/{project}/unreachable_deps_stubbifier.txt'
# with open(filePath2) as f:
#     lines2 = f.read().splitlines()
# runtime_deps_nyc = len(lines2)

# filePath3 = f'./Playground/{project}/unreachable_runtime_deps_both.txt'
# with open(filePath3) as f:
#     lines3 = f.read().splitlines()
# runtime_both = len(lines3)

# filePath4 = f'./Playground/{project}/unreachable_in_nyc_not_os.txt'
# with open(filePath4) as f:
#     lines4 = f.read().splitlines()
# in_nyc_not_os = len(lines4)

# filePath5 = f'./Playground/{project}/unreachable_in_os_not_nyc.txt'
# with open(filePath5) as f:
#     lines5 = f.read().splitlines()
# in_os_not_nyc = len(lines5)

# output_string = str(project) + "," + str(runtime_files_nyc) + "," + str(runtime_deps_nyc) + "," + str(runtime_both) + "," + str(in_nyc_not_os) + "," + str(in_os_not_nyc) + '\n'

output_string = str(project) + "," + str(lines_len) + '\n'

output_path = f'statistic.txt'
output_file = open(output_path, "a")
output_file.writelines(output_string)



# def read_dependencies(file_path):
#     with open(file_path, 'r') as file:
#         dependencies = [line.strip().split('__')[0] for line in file]
#     return dependencies

# def find_intersection(file1_path, file2_path):
#     dependencies1 = set(read_dependencies(file1_path))
#     dependencies2 = set(read_dependencies(file2_path))
#     intersection = dependencies1.intersection(dependencies2)
#     return intersection

# def write_intersection(intersection, output_file):
#     with open(output_file, 'w') as file:
#         for dep in intersection:
#             file.write(dep + '\n')

# file1_path = f'./Playground/{project}/runtime_deps__version.txt'
# file2_path = f'./Playground/{project}/unreachable_runtime_deps_removed.txt'
# output_file = f'./Playground/{project}/unreachable_runtime_deps_removed__version.txt'

# intersection = find_intersection(file1_path, file2_path)
# write_intersection(intersection, output_file)
