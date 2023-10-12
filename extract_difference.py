import sys
import os
project = sys.argv[1]
file1 = sys.argv[2]
file2 = sys.argv[3]
output_file = sys.argv[4]

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

filePath1 = f'./Playground/{project}/{file1}'
with open(filePath1) as f:
    lines1 = f.read().splitlines()
# print(len(lines1))

filePath2 = f'./Playground/{project}/{file2}'
lines2 = []
if os.path.exists(filePath2):
    with open(filePath2) as f:
        lines2 = f.read().splitlines()
# print(len(lines2))

# filePath3 = f'./Playground/{project}/direct_confirmed_deps.txt'
# lines3 = []
# if os.path.exists(filePath3):
#     with open(filePath3) as f:
#         lines3 = f.read().splitlines()
# # # print(len(lines3))

# filePath4 = f'./Playground/{project}/direct_pseudo_bloated_deps.txt'
# lines4 = []
# if os.path.exists(filePath4):
#     with open(filePath4) as f:
#         lines4 = f.read().splitlines()

# list1 = []
# for item in lines1:
#     arr = item.split(',')
#     list1.append(arr)

# list2 = []
# for item in lines2:
#     arr = item.split(',')
#     list2.append(arr)

# intersection = list(set(lines1_output).intersection(lines3))
output = list(set(lines1) - set(lines2))
# output.extend(list(set(lines3) - set(lines4)))
# print(output)
# print(len(lines3), len(intersection))

output_path = f'./Playground/{project}/{output_file}'
output_file = open(output_path, "a")
for item in output:
    # print(item)
    output_file.writelines(item + '\n')