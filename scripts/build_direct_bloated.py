import sys
import json

project = sys.argv[1]

json_path = f'./Playground/{project}/value_map.json'
f_package = open(json_path, encoding="utf-8")  
deps_dict = json.load(f_package)

direct_bloated = []

for item in deps_dict:
    if deps_dict[item]["is_direct"] == True:
        dep_id = deps_dict[item]["dep_name"] + "__" + deps_dict[item]["dep_version"]
        if dep_id not in direct_bloated:
            direct_bloated.append(dep_id)

print(direct_bloated)

direct_path = f'Playground/{project}/direct_bloated_deps.txt'
direct_deps_file = open(direct_path, "a")
for item in direct_bloated:
    direct_deps_file.writelines(item + '\n')
