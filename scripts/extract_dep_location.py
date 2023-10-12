import sys
import os
import json

project = sys.argv[1]

file_path = f'Playground/{project}/non-bloated_deps.txt'
with open(file_path) as f:
    deps = f.read().splitlines()

json_path = f'Playground/{project}/package-lock.json'
output_path = f'Playground/{project}/non-bloated_deps_location_dedup.txt'

f_package = open(json_path, encoding="utf-8")  
lockDict = json.load(f_package)
locations = lockDict["packages"]
output = []

for dep in deps:
    depinfo = dep.split('__')
    name = depinfo[0]
    version = depinfo[1]
    for key, value in locations.items():
        if name in key and value.get("version") == version:
            output.append(key)

dedup_output = []
for item in output:
    # print(item)
    modules = item.split('node_modules/')[1:]
    if len(modules) == 1:
        dedup_output.append(item)
    elif len(modules) >= 2:
        parent = 'node_modules/' + modules[0]
        if parent[:-1] not in output:
            dedup_output.append(item)

output_file = open(output_path, "a")
for item in dedup_output:
    output_file.writelines(item + '\n')