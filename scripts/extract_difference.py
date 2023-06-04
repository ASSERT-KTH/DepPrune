filePathA = f'./Logs/repo_commited_in_2023_100000_valid_entry_nodist.txt'
FilePathB = f'./Logs/repo_module_system_100000.txt'

with open(filePathA) as f:
    linesA = f.read().splitlines()
print(len(linesA))
with open(FilePathB) as f:
    linesB = f.read().splitlines()
print(len(linesB))

linesB_url = []
for line in linesB:
    item = line.split(',')
    url = item[1]
    if url in linesA:
        linesB_url.append(url)

difference = list(set(linesA).difference(linesB_url))
for item in difference:
    print(item)