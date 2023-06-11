# filePathA = f'./Logs/repo_NodeJS_100000.txt'
# FilePathB = f'./Logs/repo_100000_readme_error.txt'

# with open(filePathA) as f:
#     linesA = f.read().splitlines()
# print(len(linesA))
# with open(FilePathB) as f:
#     linesB = f.read().splitlines()
# print(len(linesB))

# linesB_url = []
# for line in linesB:
#     item = line.split(',')
#     url = item[1]
#     if url in linesA:
#         linesB_url.append(url)

# difference = list(set(linesA).difference(linesB_url))
# for item in difference:
#     print(item)

filePath1 = f'./Logs/repo_NodeJS_100000.txt'
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

print(len(difference))
for item in difference:
    # line = ",".join(item) + "\n"
    # collection_file.writelines(line)
    arr = item.split(',')
    print(arr[0])