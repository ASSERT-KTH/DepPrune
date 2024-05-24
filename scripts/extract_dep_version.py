import sys
import os
import json

project = sys.argv[1]
basement = "Playground"

opened_file_path = f'{basement}/{project}/opened_runtime_deps.txt'
with open(opened_file_path) as f:
    opened_deps = f.read().splitlines()

bloated_file_path = f'{basement}/{project}/unreachable_runtime_deps_removed.txt'
with open(bloated_file_path) as f:
    bloated_deps = f.read().splitlines()
    
opened = []
bloated = []

# read lock json
json_path = f'{basement}/{project}/package-lock.json'
f_package = open(json_path, encoding="utf-8")  
jsonData = json.load(f_package)
pckData = jsonData['packages']


# opened_version_output_path = f'{basement}/{project}/opened_deps_version.txt'
# bloated_version_output_path = f'{basement}/{project}/bloated_deps_version.txt'
opened_bloated_deps_output_path = f'{basement}/{project}/opened_bloated_deps_version.txt'
bloated_not_opened_deps_output_path = f'{basement}/{project}/bloated_unopened_deps_version.txt'

def extract_dep_name(path):
    parts = path.split("node_modules/")

    if len(parts) > 1:
        return parts[-1]
    else:
        return path

for key, value in pckData.items():
    if key in opened_deps and value.get("version"):
        dep_name = extract_dep_name(key)
        dep_info = dep_name + "__" + value.get("version")
        opened.append(dep_info)
    
    if key in bloated_deps and value.get("version"):
        dep_name = extract_dep_name(key)
        dep_info = dep_name + "__" + value.get("version")
        bloated.append(dep_info)

opened_bloated = list(set(opened).intersection(bloated))
bloated_not_opened = list(set(bloated) - set(opened))

print("opened_deps", len(opened_bloated))
print("bloated_deps", len(bloated_not_opened))


opened_bloated_file = open(opened_bloated_deps_output_path, "a")
for item in opened_bloated:
    opened_bloated_file.writelines(item + '\n')

bloated_not_opened_file = open(bloated_not_opened_deps_output_path, "a")
for item in bloated_not_opened:
    bloated_not_opened_file.writelines(item + '\n')