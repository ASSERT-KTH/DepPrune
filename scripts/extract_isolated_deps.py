import sys
import json
import os
import subprocess
import ast

project = sys.argv[1]

filePath = f'./Playground/{project}/dependent-files.json'
f_package = open(filePath, encoding="utf-8")  
clientsDict = json.load(f_package)

deps_path = f'./Playground/{project}/potential-deps.txt'
with open(deps_path) as f:
    potential_deps = f.read().splitlines()

old_path_pre = f"/data/js-variants/multee/Playground/{project}/" 
new_path_pre = f"/data/js-variants/multee/TestCollection/{project}/"

client_files_path = f"./Playground/{project}/non-isolated-clients.json"
non_isolated_json = {}

def match(files, deps):
    matchedFiles = []
    # print("files: " + str(files))
    # print("deps: " + str(deps))
    for line in files:
        nearestDep = "node_modules" + line.split("node_modules")[-1]
        for dep in deps:
            if dep in nearestDep and line not in matchedFiles:
                matchedFiles.append(line)
    return matchedFiles

isolated_file = open(f"./Playground/{project}/isolated-deps.txt", "a")
non_isolated_file = open(f"./Playground/{project}/non-isolated-deps.txt", "a")
for line in potential_deps:
    depInfo = line.split("__")
    depName = depInfo[0]
    depVersion = depInfo[1]
    for key, value in clientsDict.items():
        if key == depName:
            targetFiles = []
            if len(value) != 0:
                clientFiles = value
            # if len(value) != 0:
            #     print(key)
                result = subprocess.run(["python3", "scripts/exclude_indirect_dep.py", depName, depVersion, project], stdout=subprocess.PIPE, text=True)
                clientDeps = ast.literal_eval(result.stdout)
                targetFiles = match(clientFiles, clientDeps)
                # print(targetFiles)
            if len(targetFiles) == 0:
                print(line + "," + str(len(targetFiles)))
                isolated_file.writelines(line+"\n")
            if len(targetFiles) != 0:
                print(line + "," + str(len(targetFiles)))
                non_isolated_json[line] = targetFiles
                non_isolated_file.writelines(line + "," + str(len(targetFiles))+"\n")

with open(client_files_path, 'w') as file:
    json.dump(non_isolated_json, file, indent=4)