filePath1 = f'./Logs/repo_100000_branch.txt'
with open(filePath1) as f:
    lines1 = f.read().splitlines()

filePath2 = f'./Logs/repo_module_system_100000.txt'
with open(filePath2) as f:
    lines2 = f.read().splitlines()

list1 = []
for item in lines1:
    arr = item.split(',')
    list1.append(arr)

list2 = []
for item in lines2:
    arr = item.split(',')
    list2.append(arr)

intersection = [arr1 + arr2 for arr1 in list1 for arr2 in list2 if arr1[1] == arr2[0] and arr2[2] == " NodeJS"]

collection_file = open("./Logs/repo_NodeJS_100000.txt", "a")
for item in intersection:
    line = ",".join(item) + "\n"
    collection_file.writelines(line)
    