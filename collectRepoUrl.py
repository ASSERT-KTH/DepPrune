import sys

project = sys.argv[1]
filePath = f'./Data/{project}/{project}_dependants_url.txt'
newFilePath = f'./Data/{project}/{project}_dependants_url_100.txt'

with open(filePath) as f:
    lines = f.read().splitlines()

lines = list(dict.fromkeys(lines))

newFile = open(newFilePath, 'w')
for line in lines:
    newFile.writelines(line + '\n')
newFile.close()
