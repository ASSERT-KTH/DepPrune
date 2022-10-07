import sys
import os
import subprocess

project = sys.argv[1]

unbloatedDeps = []

totalNodesPath = f'{os.getcwd()}/Data/{project}/dependency-tree-list.txt'
bloatedNodesPath = f'{os.getcwd()}/Data/{project}/{project}_bloated_nodes.txt'
bloatedUnpureDepsPath = f'{os.getcwd()}/Data/{project}/{project}_bloated_deps.txt'

totalNodes = set(open(totalNodesPath, 'r').readlines())
bloatedNodes = set(open(bloatedNodesPath, 'r').readlines())
bloatedUnpureDeps = set(open(bloatedUnpureDepsPath, 'r').read().splitlines())


def cutTotalStr(str):
    return str[52:]
def cutBloatedStr(str):
    return str[36:]

totalFiles = list(map(cutTotalStr, totalNodes))
bloatFiles = list(map(cutBloatedStr, bloatedNodes))

diffNodes = list(set(totalFiles).difference(set(bloatFiles)))

for nodePath in diffNodes:
    pathArr = nodePath.split('/')
    if ('node_modules' in pathArr):
        nodeMIdx = pathArr.index('node_modules')
        depName = pathArr[nodeMIdx + 1]
        if (depName not in unbloatedDeps):
            unbloatedDeps.append(depName)

print(unbloatedDeps)
print(bloatedUnpureDeps)

diffDeps = list(set(bloatedUnpureDeps).difference(set(unbloatedDeps)))
print(diffDeps)

pureBloatedDepsPath = f'./Data/{project}/{project}_bloated_pure_deps.txt'
pureBloatedDepsFile = open(pureBloatedDepsPath, 'w')
for diff in diffDeps:
    print(diff)
    pureBloatedDepsFile.writelines(diff + '\n')
pureBloatedDepsFile.close()