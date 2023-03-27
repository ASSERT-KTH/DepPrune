import sys
import json
import os

project = sys.argv[1]
# Read transitive dependencies from /Data/packageName
filePath = f'./Data/{project}/{project}_deps_bloated_transitive.txt'
with open(filePath) as f:
    lines = f.read().splitlines()

# Modify package.json file

filePath_package = f'./VariantsPureDep/{project}/variant_deps/{project}/package.json'    
f_package = open(filePath_package, encoding="utf-8")  
packageDict = json.load(f_package)

exDict = {}

for item in lines:
    exDict[item] = "prod"
print(exDict)

packageDict['exclusions'] = exDict

with open(filePath_package, 'w') as f:
    json.dump(packageDict, f)