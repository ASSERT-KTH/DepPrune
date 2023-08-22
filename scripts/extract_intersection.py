import sys
project = sys.argv[1]

filePath1 = f'./Playground/{project}/potential-deps.txt'
with open(filePath1) as f:
    lines1 = f.read().splitlines()
print(len(lines1))

filePath2 = f'./Playground/{project}/direct_bloated_deps.txt'
with open(filePath2) as f:
    lines2 = f.read().splitlines()
print(len(lines2))
# print(project + "," + str(len(lines2)))

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


collection_file = open(f'./Playground/{project}/direct-isolated-deps.txt', "a")
for item in intersection:
    # line = ",".join(item)
    collection_file.writelines(item+"\n")
    