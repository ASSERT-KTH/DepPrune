import sys
import os
project = sys.argv[1]
file1 = sys.argv[2]
file2 = sys.argv[3]
output_file = sys.argv[4]

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

output = list(set(lines1) - set(lines2))

output_path = f'./Playground/{project}/{output_file}'
output_file = open(output_path, "a")
for item in output:
    # print(item)
    output_file.writelines(item + '\n')