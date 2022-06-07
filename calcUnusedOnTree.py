import sys
import os

project = sys.argv[1]
total = []
onTree = []

projectPath = os.getcwd() + '/Playground/' + project
totalUnusedFilesPath = projectPath + '/unused-files.txt'
onTreeFilesPath = projectPath + '/dependency-tree-list.txt'

totalF = open(totalUnusedFilesPath, 'r')
for line in totalF.readlines():
    total.append(line)

onTreeF = open(onTreeFilesPath, 'r')
for line in onTreeF.readlines():
    onTree.append(line)

unusedOnTree = list(set(total).intersection(set(onTree)))

for file in unusedOnTree:
    print(file)

print(len(unusedOnTree))
