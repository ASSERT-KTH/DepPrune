import sys
import os

project = sys.argv[1]

debloatStrategy = ['functions', 'files', 'deps']
unbloatedDeps = []
bloatedDeps = []
bloatedPureDeps = []
pureBloatedNodes = []

# get all nodes on the dependency tree
totalNodesPath = f'{os.getcwd()}/Playground/{project}/dependency-tree-list.txt'
totalNodes = set(open(totalNodesPath, 'r').readlines())

# get all bloated nodes
totalBloatedNodesPath = f'{os.getcwd()}/Playground/{project}/unused-files.txt'
if not os.path.exists(totalBloatedNodesPath):
    totalBloatedNodes = []
else:
    totalBloatedNodes = set(open(totalBloatedNodesPath, 'r').readlines())


def cutTotalStr(str):
    return str[52:]
def cutBloatedStr(str):
    return str[36:]

def getDepByNode(nodeStr):
    pathArr = nodeStr.split('/')
    if ('node_modules' in pathArr):
        nodeMIdx = pathArr.index('node_modules')
        depName = pathArr[nodeMIdx + 1]
        return depName
    return ''

# diffNodes: nodes on the tree that are not bloated
diffNodes = list(set(totalNodes).difference(set(totalBloatedNodes)))

# interNodesWithOwn: nodes on the tree that are bloated
interNodesWithOwn = list(set(totalNodes).intersection(set(totalBloatedNodes)))
interNodes = [s for s in interNodesWithOwn if 'node_modules' in s]


# record deps that is used on tree, even though they have bloated nodes.
for nodePath in diffNodes:
    depName = getDepByNode(nodePath)
    if (depName not in unbloatedDeps and depName != ''):
        unbloatedDeps.append(depName)

# record deps that have bloated node(s) on tree
for nodePath in interNodes:
    depName = getDepByNode(nodePath)
    if (depName not in bloatedDeps):
        bloatedDeps.append(depName)

# print('bloatedDeps', bloatedDeps)

# record deps that are pure bloated meaning that all files in the deps are bloated
pureBloatedDeps = list(set(bloatedDeps).difference(set(unbloatedDeps)))
print('bloatedPureDeps', pureBloatedDeps)

# record nodes that are from pure bloated deps
for nodePath in interNodes:
    depName = getDepByNode(nodePath)
    if depName in pureBloatedDeps:
        pureBloatedNodes.append(nodePath)
# print('pureBloatedNodes', pureBloatedNodes)


# pureBloatedDepsPath = f'./Data/{project}/{project}_pure_bloated_deps.txt'
# pureBloatedDepsFile = open(pureBloatedDepsPath, 'w')
# for dep in pureBloatedDeps:
#     pureBloatedDepsFile.writelines(dep + '\n')
# pureBloatedDepsFile.close()

# pureBloatedNodesPath = f'./Data/{project}/{project}_pure_bloated_nodes.txt'
# pureBloatedNodesFile = open(pureBloatedNodesPath, 'w')
# for node in pureBloatedNodes:
#     pureBloatedNodesFile.writelines(node)
# pureBloatedNodesFile.close()

bloatedNodesOnTreePath = f'./Data/{project}/{project}_bloated_nodes_on_tree.txt'
bloatedNodesOnTreeFile = open(bloatedNodesOnTreePath, 'w')
for node in interNodes:
    bloatedNodesOnTreeFile.writelines(node)
bloatedNodesOnTreeFile.close()