import json
import sys

folder = sys.argv[1]
filePath = f'Original/{folder}/package.json'
f = open(filePath, encoding="utf-8")
packageDict = json.load(f)


if 'type' in packageDict and packageDict['type'] == "module":
    print(folder)