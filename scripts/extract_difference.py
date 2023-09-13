import sys
import os
project = sys.argv[1]

# filePathA = f'./Logs/repo_NodeJS_100000.txt'
# FilePathB = f'./Logs/repo_100000_readme_error.txt'

# with open(filePathA) as f:
#     linesA = f.read().splitlines()
# print(len(linesA))
# with open(FilePathB) as f:
#     linesB = f.read().splitlines()
# print(len(linesB))

# linesB_url = []
# for line in linesB:
#     item = line.split(',')
#     url = item[1]
#     if url in linesA:
#         linesB_url.append(url)

# difference = list(set(linesA).difference(linesB_url))
# for item in difference:
#     print(item)

# filePath1 = f'./Playground/{project}/total_deps.txt'
# with open(filePath1) as f:
#     lines1 = f.read().splitlines()
# lines1_temp = []
# for item in lines1:
#     if "UNMET" not in item:
#         arr = item.rsplit("@", 1)
#         output_str = arr[0] + "__" + arr[1]
#         lines1_temp.append(output_str)
# # The following line is important to filter out the repeatedly installed same dependency.
# lines1_output = list(set(lines1_temp)) 

# print(len(lines1_output))

filePath1 = f'./Playground/{project}/total__deps.txt'
with open(filePath1) as f:
    lines1 = f.read().splitlines()
# print(len(lines1))

filePath2 = f'./Playground/{project}/indirect_confirmed_deps.txt'
with open(filePath2) as f:
    lines2 = f.read().splitlines()
# print(len(lines2))

filePath3 = f'./Playground/{project}/direct_confirmed_deps.txt'
lines3 = []
if os.path.exists(filePath3):
    with open(filePath3) as f:
        lines3 = f.read().splitlines()
# print(len(lines3))

# list1 = []
# for item in lines1:
#     arr = item.split(',')
#     list1.append(arr)

# list2 = []
# for item in lines2:
#     arr = item.split(',')
#     list2.append(arr)

# intersection = list(set(lines1_output).intersection(lines3))
output = list(set(lines1) - set(lines2) - set(lines3))
print(len(output))
# print(len(lines3), len(intersection))

output_path = f'./Playground/{project}/non-bloated_deps.txt'
output_file = open(output_path, "a")
for item in output:
    # print(item)
    output_file.writelines(item + '\n')