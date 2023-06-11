filePath1 = f'./Logs/repo_100000_readme.txt'
with open(filePath1) as f:
    lines1 = f.read().splitlines()

filePath2 = f'./Logs/repo_100000_readme_error.txt'
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

for arr1 in list1:
    for arr2 in list2:
        if arr1[1] == arr2[0] and arr2[1] == ' no readme.':
            list2.remove(arr2)


collection_file = open("./Logs/repo_100000_readme_error_rest.txt", "a")
for item in list2:
    line = ",".join(item) + "\n"
    collection_file.writelines(line)
    