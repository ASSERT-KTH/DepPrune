import sys
import json
import os

project = sys.argv[1]

bloatedFilePath = f'./Data/{project}/{project}_pure_bloated_nodes.txt'
with open(bloatedFilePath) as f:
    bloatedFiles = f.read().splitlines()

depDict = {
    "package": project
}

for item in bloatedFiles:
    depDict[item] = []

# print(depDict)

jsonPath = f'./Bigdata/{project}_wrapped-dependency-tree.json'
jFile = open(jsonPath, encoding="utf-8")  
depTreeDictRaw = json.load(jFile)

def parse_wrapped_tree(treeDict, filename):
    if not treeDict['path']:
        return

    if treeDict['path'] == filename and treeDict['parent'] not in depDict[filename]:
        depDict[filename].append(treeDict['parent'])

    if len(treeDict['children']) != 0:
        for item in treeDict['children']:
            parse_wrapped_tree(item, filename)

    return depDict


for item in bloatedFiles:
    parse_wrapped_tree(depTreeDictRaw, item)


dependentJson = f'./Bigdata/{project}_bloated_dependents.json'
with open(dependentJson, 'w') as json_file:
  json.dump(depDict, json_file)
