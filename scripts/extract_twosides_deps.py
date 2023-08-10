import sys
import os

project = sys.argv[1]

file_path1 = f'./Playground/{project}/potential-deps.txt'
with open(file_path1) as f:
    lines1 = f.read().splitlines()

file_path2 = f'./Playground/{project}/reachable-deps.txt'
with open(file_path2) as f:
    lines2 = f.read().splitlines()

list1 = []
for item in lines1:
    arr = item.split('__')
    if arr[0] not in list1:
        list1.append(arr[0])

list2 = []
for item in lines2:
    arr = item.split('__')
    if arr[0] not in list2:
        list2.append(arr[0])

intersection = list(set(list1).intersection(set(list2)))
print(project + "," + str(len(intersection)))

output_path = f'./Playground/{project}/twosides-deps.txt'
collection_file = open(output_path, "a")
for item in intersection:
    # line = ",".join(item)
    collection_file.writelines(item+"\n")
