import sys
import os
import json

project = sys.argv[1]

used_file_path = f'Playground/{project}/used-files.txt'
with open(used_file_path) as f:
    used_lines = f.read().splitlines()

unused_file_path = f'Playground/{project}/unused-files.txt'
with open(unused_file_path) as f:
    unused_lines = f.read().splitlines()

def get_direct_deps(json_path):
    f_package = open(json_path, encoding="utf-8")  
    packageDict = json.load(f_package)
    if "dependencies" in packageDict.keys():
        directDeps = list(packageDict['dependencies'])
        print('directDeps: ', directDeps)
        return directDeps

def get_dep_name(file_path):
    dep_name = file_path.split("/node_modules/")[1].split("/")[0]
    return dep_name

reachable_deps_arr = []
for path in used_lines:
    if "/node_modules/" in path:
        dep_name = get_dep_name(path)
        if dep_name not in reachable_deps_arr:
            reachable_deps_arr.append(dep_name)

print("There are ", len(reachable_deps_arr), "reachable dependencies in ", project)
reachable_path = f'Playground/{project}/reachable-deps.txt'
reachable_file = open(reachable_path, "a")
for item in reachable_deps_arr:
    reachable_file.writelines(item + '\n')


unused_deps_arr = []
for path in unused_lines:
    if "/node_modules/" in path:
        dep_name = get_dep_name(path)
        if dep_name not in unused_deps_arr:
            unused_deps_arr.append(dep_name)

print("There are ", len(unused_deps_arr), "unused dependencies in ", project)
unused_path = f'Playground/{project}/unused-deps.txt'
unused_deps_file = open(unused_path, "a")
for item in unused_deps_arr:
    unused_deps_file.writelines(item + '\n')

json_path = f'Playground/{project}/package.json'
direct_deps = get_direct_deps(json_path)
direct_path = f'Playground/{project}/direct-deps.txt'
direct_file = open(direct_path, "a")
for item in direct_deps:
    direct_file.writelines(item + '\n')

potential_deps = list(set(unused_deps_arr).difference(reachable_deps_arr))
print("There are ", len(potential_deps), "potential bloated dependencies in ", project)
potential_path = f'Playground/{project}/potential-deps.txt'
potential_deps_file = open(potential_path, "a")
for item in potential_deps:
    potential_deps_file.writelines(item + '\n')

