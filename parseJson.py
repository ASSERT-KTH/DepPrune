import json
import sys

folder = sys.argv[1]
filePath = f'Original/{folder}/package.json'
f = open(filePath, encoding="utf-8")
packageDict = json.load(f)

depFilePath = f'dependencies.txt'
devDepFilePath = f'devDependencies.txt'

if 'dependencies' in packageDict:
    dependencies = packageDict['dependencies']
    depFile = open(depFilePath, 'a')
    for key in dependencies.keys():
        depFile.writelines(folder + ',' + key + '\n')
    depFile.close()
    

if 'devDependencies' in packageDict:
    devDependencies = packageDict['devDependencies']
    devDepFile = open(devDepFilePath, 'a')
    for key in devDependencies.keys():
        devDepFile.writelines(folder + ',' + key + '\n')
    devDepFile.close()