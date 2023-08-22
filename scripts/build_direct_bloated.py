# Take potential deps and direct deps as input,
# parse the package.json for each node_modules/directDeps, get the version and compare it if it is a potential bloated one.

import sys
import json
import os

project = sys.argv[1]

direct_path = f'Playground/{project}/direct-deps.txt'
with open(direct_path) as f:
    direct_deps = f.read().splitlines()

potential_path = f'Playground/{project}/potential-deps.txt'
with open(potential_path) as f:
    potential_deps = f.read().splitlines()

def get_dep_version(file_path):
    if not os.path.exists(file_path):
        return None
    f_package = open(file_path, encoding="utf-8")  
    packageDict = json.load(f_package)
    dep_info = {}
    if "version" in packageDict.keys():
        version = packageDict.get("version")
        return version
    return None

direct_deps_info = []
for dep in direct_deps:
    package_json_path = f'Playground/{project}/node_modules/{dep}/package.json'
    dep_version = get_dep_version(package_json_path)
    dep_info = dep + "__" + dep_version
    direct_deps_info.append(dep_info)

# print(direct_deps_info)

direct_bloated = []
for item in direct_deps_info:
    if item in potential_deps:
        direct_bloated.append(item)

print(direct_bloated)

info_path = f'Playground/{project}/direct_deps_info.txt'
info_file = open(info_path, "a")
for item in direct_deps_info:
    info_file.writelines(item + '\n')

direct_path = f'Playground/{project}/direct_bloated_deps.txt'
direct_deps_file = open(direct_path, "a")
for item in direct_bloated:
    direct_deps_file.writelines(item + '\n')
