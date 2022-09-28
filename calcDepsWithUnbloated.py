import sys
import os

project = sys.argv[1]
unpureBloatedDeps = []

totalNodesPath = os.getcwd() + '/Playground/' + project + '/dependency-tree-list.txt'
bloatedNodesPath = os.getcwd() + '/Data/' + project + '/' + project + '_bloated_nodes.txt'

totalNodes = set(open(totalNodesPath, 'r').readlines())
bloatedNodes = set(open(bloatedNodesPath, 'r').readlines())

diffNodes = list(set(totalNodes).difference(set(bloatedNodes)))


for nodePath in diffNodes:
    pathArr = nodePath.split('/')
    nodeMIdx = pathArr.index('node_modules')
    depName = pathArr[nodeMIdx + 1]
    if (depName not in unpureBloatedDeps):
        unpureBloatedDeps.append(depName)

print(len(unpureBloatedDeps))
print(unpureBloatedDeps)
