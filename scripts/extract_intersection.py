import sys
import os

project = sys.argv[1]

filePath1 = f'./Playground/{project}/direct-confirmed-deps.txt'
lines1 = []
if os.path.exists(filePath1):
    with open(filePath1) as f:
        lines1 = f.read().splitlines()
# print(len(lines1))

filePath2 = f'./Playground/{project}/direct_indirect_bloated_deps.txt'
lines2 = []
if os.path.exists(filePath2):
    with open(filePath2) as f:
        lines2 = f.read().splitlines()
# print(len(lines1))

# filePath2 = f'./Playground/{project}/isolated-deps_from_total.txt'
# with open(filePath2) as f:
#     lines2 = f.read().splitlines()
# print(len(lines2))

# deduped_deps = []
# for dep in lines2:
#     dep_arr = dep.split("__")
#     deduped_dep = dep_arr[0] + "@" + dep_arr[1] + " deduped"
#     if deduped_dep in lines1:
#         deduped_deps.append(dep)
# print(len(deduped_deps))

# output_deps = list(set(lines1) - set(lines2))
# print(project + "," + str(len(output_deps)))
# print(output_deps)

# list1 = []
# intersection = []
# for item in lines1:
#     arr = item.split(',')
#     if arr[0] in lines2:
#         intersection.append(item)

# list2 = []
# for item in lines2:
#     arr = item.split(',')
#     list2.append(item)

# intersection = [arr1 for arr1 in list1 for arr2 in lines2 if arr1[0] == arr2[0]]
# print(len(intersection))

intersection = list(set(lines1).intersection(lines2))
print(project + "," + str(len(intersection)))

# output_file = open(f'./Playground/{project}/isolated_reachable_deps.txt', "a")
# for item in intersection:
#     # line = ",".join(item)
#     output_file.writelines(item+"\n")
    