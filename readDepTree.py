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
resultList = []
def get_depth_of_dep(dictionary, depArr):
    global level
    global resultList
    for key, value in dictionary.items():
        if key == "dependencies" and isinstance(value, dict):
            level = level + 1
            childDict = value
            output = list(childDict.keys())
            for item in output:
                if item in depArr:
                    pair = {
                        'name': item,
                        'level': level 
                    }
                    resultList.append(pair)
                    transDeps.remove(item)
            for itemKey, itemValue in childDict.items():
                get_depth_of_dep(itemValue, transDeps)
            level = level - 1

if __name__ == '__main__':
    get_depth_of_dep(productionDict, transDeps)
    resultPath = f'./Data/{project}/{project}_deps_bloated_level.txt'  
    resultFile = open(resultPath, 'a')
    for item in resultList:
        string = f"{item['name']},{item['level']}"
        resultFile.writelines(string + '\n')
    resultFile.close()