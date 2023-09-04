import sys
import os

project = sys.argv[1]

lines1 = []
file_path1 = f'./Playground/{project}/direct_confirmed_deps.txt'
if os.path.exists(file_path1):
    with open(file_path1) as f:
        lines1 = f.read().splitlines()


file_path2 = f'./Playground/{project}/indirect_confirmed_deps.txt'
with open(file_path2) as f:
    lines2 = f.read().splitlines()

total_confirmed_deps = list(set(lines1).union(set(lines2)))
# print(len(total_confirmed_deps))

file_path3 = f'./Playground/{project}/reachable-deps.txt'
with open(file_path3) as f:
    lines3 = f.read().splitlines()
# print(len(lines3))


reachable = []
for item in total_confirmed_deps:
    arr = item.split('__')
    if arr[0] not in reachable:
        reachable.append(arr[0])

confirmed = []
for item in lines3:
    arr = item.split('__')
    if arr[0] not in confirmed:
        confirmed.append(arr[0])

intersection = list(set(reachable).intersection(set(confirmed)))
print(project + "," + str(len(intersection)))

output_path = f'./Playground/{project}/reachable_confirmed_deps.txt'
collection_file = open(output_path, "a")
for item in intersection:
    # line = ",".join(item)
    collection_file.writelines(item+"\n")
