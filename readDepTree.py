import sys
import json
import os

project = sys.argv[1]

# transDepsPath = f'./Data/{project}/{project}_deps_bloated_transitive.txt'
depsPath = f'./Data/{project}/{project}_pure_bloated_deps.txt'
if not os.path.exists(depsPath):
    print(project + ' has no bloated deps')
    exit()

with open(depsPath) as f:
    transDeps = f.read().splitlines()

treePathDeps = f'./Original/{project}/productionDependenciesNew.json'
t_deps = open(treePathDeps, encoding="utf-8")
productionDict = json.load(t_deps)

level = 0
resultDict = {}
deptreeDepth = 0


def get_depth_of_dep(dictionary):
    global level
    global resultDict
    global deptreeDepth
    for key, value in dictionary.items():
        if key == "dependencies" and isinstance(value, dict):
            level = level + 1
            childDict = value
            isLeaf = False
            # output = list(childDict.keys())
            # for item in output:
            #     if item in depArr:
            #         pair = {
            #             'name': item,
            #             'level': level 
            #         }
            #         resultList.append(pair)
            #         transDeps.remove(item)
            for itemKey, itemValue in childDict.items():
                if isinstance(itemValue, dict):
                    itemValueKeys = list(itemValue.keys())
                    if "dependencies" not in itemValueKeys:
                        isLeaf = True
                        if deptreeDepth < level:
                            deptreeDepth = level
                if itemKey in transDeps:
                    # print(itemKey)
                    if itemKey not in resultDict:
                        resultDict[itemKey] = {
                            'name': itemKey,
                            'level': level,
                            'isLeaf': isLeaf
                        }
                    else:
                        if resultDict[itemKey].get('level') > level:
                            resultDict[itemKey]['level'] = level
                    # print(resultDict)
                get_depth_of_dep(itemValue)
            level = level - 1

if __name__ == '__main__':
    get_depth_of_dep(productionDict)
    resultPath = f'./Data/{project}/{project}_deps_bloated_level_with_leaf.txt'  
    resultFile = open(resultPath, 'a')
    # print(resultDict)
    for key, value in resultDict.items():
        # print("item", key)
        string = f"{value['name']},{value['level']},{value['isLeaf']}"
        resultFile.writelines(string + '\n')
    resultFile.close()
    print(project, deptreeDepth)