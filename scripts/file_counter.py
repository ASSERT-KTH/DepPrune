import sys

filePath = sys.argv[1]
project = sys.argv[2]

# with open(filePath) as f:
#     lines = f.read().splitlines()

projFileNum = 0
depFileNum = 0

# for line in lines:
#     print(line)
if 'node_modules' in filePath:
    depFileNum += 1
else:
    projFileNum += 1

# totalFilePath = f'total_files_number.txt'
# totalFile = open(totalFilePath, 'a')
# countStr = project + ',' + str(projFileNum) + ',' + str(depFileNum) + '\n'
# totalFile.writelines(countStr)
# totalFile.close()

