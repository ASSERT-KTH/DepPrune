import sys
import json
import os
import subprocess

project = sys.argv[1]

filePath = f'./Bigdata/{project}_bloated_dependents.json'
f_package = open(filePath, encoding="utf-8")  
depDict = json.load(f_package)

def get_depname_by_path(path):
    pathArr = path.split('/')
    return pathArr[7]

oldPathPre = f"/data/js-variants/multee/Playground/{project}/" 
newPathPre = f"/data/js-variants/multee/VariantsPureDep/{project}/variant_deps/{project}/" 

for key, value in depDict.items():
    if (key != 'package'):
        depName = get_depname_by_path(key)
        print(depName)
        for item in value:
            depVariantItem = item.replace(oldPathPre, newPathPre)
            print(depVariantItem)
            if os.path.exists(depVariantItem):
                result = subprocess.run(["node", "remove_deps_originally.js", depVariantItem, depName])
                print(result)



        

