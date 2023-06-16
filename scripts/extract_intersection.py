filePath1 = f'./Logs/repo_100000_coverage_github.txt'
with open(filePath1) as f:
    lines1 = f.read().splitlines()

filePath2 = f'./Logs/rerun_test.txt'
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

intersection = [arr1 for arr1 in list1 for arr2 in list2 if arr1[1] == arr2[0] and "ember-" not in arr1[0]]
print(len(intersection))

collection_file = open("./Logs/rerun_test_coverage_2020.txt", "a")
for item in intersection:
    line = ",".join(item) + "\n"
    collection_file.writelines(line)
    