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

projPath = 'Data/'+ project + '/' + project + '_bloated_nodes_on_tree.txt'
fileUnusedOnTree = open(projPath, 'w')
for file in unusedOnTree:
    print(file)
    fileUnusedOnTree.writelines(file)
fileUnusedOnTree.close()

print(len(unusedOnTree))
