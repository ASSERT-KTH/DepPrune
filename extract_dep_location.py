import sys
import os
import json

project = sys.argv[1]
folder = sys.argv[2]

basement = "Playground"

file_path = f'{basement}/{project}/{folder}.txt'
with open(file_path) as f:
    deps = f.read().splitlines()

json_path = f'{basement}/{project}/package-lock.json'
output_path = f'{basement}/{project}/{folder}_locations.txt'


def gen_ancesstor(input_array):
    hierarchical_paths = []

    current_path = ""

    for item in input_array:
        current_path += "node_modules/" + item
        hierarchical_paths.append(current_path.rstrip('/'))

    return hierarchical_paths



f_package = open(json_path, encoding="utf-8")  
lockDict = json.load(f_package)
locations = lockDict["packages"]
output = []

for dep in deps:
    depinfo = dep.split('__')
    name = depinfo[0]
    version = depinfo[1]
    for key, value in locations.items():
        cur_dep = key.split('node_modules/')[-1]
        if name == cur_dep and value.get("version") == version and "dev" not in value:
            output.append(key)

dedup_output = []
for item in output:
    # print(item)
    modules = item.split('node_modules/')[1:]
    if len(modules) == 1:
        dedup_output.append(item)
    elif len(modules) >= 2:
        ancesstors = gen_ancesstor(modules[:-1])
        is_anc_in = False
        for ancesstor in ancesstors:
            if ancesstor in output:
                is_anc_in = True
        if not is_anc_in:
            dedup_output.append(item)

output_file = open(output_path, "a")
for item in dedup_output:
    output_file.writelines(item + '\n')