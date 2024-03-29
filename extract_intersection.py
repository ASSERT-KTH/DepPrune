import sys
import os

project = sys.argv[1]
file1 = sys.argv[2]
file2 = sys.argv[3]
output_path = sys.argv[4]

filePath1 = f'./Playground/{project}/{file1}'
lines1 = []
if os.path.exists(filePath1):
    with open(filePath1) as f:
        lines1 = f.read().splitlines()

# print(len(lines1))

filePath2 = f'./Playground/{project}/{file2}'
lines2 = []
if os.path.exists(filePath2):
    with open(filePath2) as f:
        lines2 = f.read().splitlines()
# print(len(lines2))

intersection = list(set(lines1).intersection(lines2))
print(project + "," + str(len(intersection)))

# output_file = open(f'./Playground/{project}/{output_path}', "a")
# for item in intersection:
#     # line = ",".join(item)
#     output_file.writelines(item+"\n")
    