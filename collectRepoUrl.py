import sys

# project = sys.argv[1]
# filePath = f'./Data/{project}/{project}_dependants_url.txt'
# newFilePath = f'./Data/{project}/{project}_dependants_url_100.txt'

# deduplicate
# filePath = f'top3000.txt'
# newFilePath = f'top3000_new.txt'

# with open(filePath) as f:
#     lines = f.read().splitlines()

# lines = list(dict.fromkeys(lines))

# newFile = open(newFilePath, 'w')
# for line in lines:
#     newFile.writelines(line + '\n')
# newFile.close()

filePath = f'top3000_url.txt'
newFilePath = f'top3000_url_deduplicated.txt'
duplicatedFilePath = f'top3000_url_duplicated.txt'
urlList = []
duplicatedList = []

with open(filePath) as f:
    lines = f.read().splitlines()

newFile = open(newFilePath, 'w')
duplicatedFile = open(duplicatedFilePath, 'a')

for line in lines:
    row = line.split(',')
    url = row[1]
    if url == 'null' or url == 'undefined' or url == 'https://github.com/null':
        continue 
    if url in urlList:
        duplicatedFile.writelines(line + '\n')
    if url not in urlList:
        urlList.append(url)
        newFile.writelines(line + '\n')

newFile.close()
duplicatedFile.close()