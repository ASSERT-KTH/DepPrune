# filePath1 = f'./Logs/target_103_loc_loc.txt'
filePath1 = f'./Logs/target_103_loc_loc.txt'
with open(filePath1) as f:
    lines1 = f.read().splitlines()
print(len(lines1))

filePath2 = f'./Logs/target_70_packages.txt'
with open(filePath2) as f:
    lines2 = f.read().splitlines()
print(len(lines2))

list1 = []
intersection = []
for item in lines1:
    arr = item.split(',')
    if arr[0] in lines2:
        intersection.append(item)

# list2 = []
# for item in lines2:
#     arr = item.split(',')
#     list2.append(item)

# intersection = [arr1 for arr1 in list1 for arr2 in lines2 if arr1[0] == arr2[0]]
print(len(intersection))

# intersection = list(set(lines1).difference(lines2))
# print(len(intersection))

collection_file = open("./Logs/temp_test_intersection.txt", "a")
for item in intersection:
    # line = ",".join(item)
    collection_file.writelines(item+"\n")
    