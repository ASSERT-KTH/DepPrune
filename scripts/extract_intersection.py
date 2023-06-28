filePath1 = f'./Logs/rerun_test_1000_commits.txt'
with open(filePath1) as f:
    lines1 = f.read().splitlines()
print(len(lines1))

filePath2 = f'./Logs/temp_test.txt'
with open(filePath2) as f:
    lines2 = f.read().splitlines()
print(len(lines2))

list1 = []
for item in lines1:
    arr = item.split(',')
    list1.append(arr)

list2 = []
for item in lines2:
    arr = item.split(',')
    list2.append(arr)


intersection = [arr1 for arr1 in list1 for arr2 in list2 if arr1[1] == arr2[0]]
print(len(intersection))

# intersection = list(set(lines1).difference(lines2))
# print(len(intersection))

collection_file = open("./Logs/temp_test_intersection.txt", "a")
for item in intersection:
    line = ",".join(item) + "\n"
    collection_file.writelines(line)
    