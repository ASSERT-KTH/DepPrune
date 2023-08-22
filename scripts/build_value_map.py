import sys
import os
import json
import re

project = sys.argv[1]

# input: 
# used-files.txt
# unused-files.txt
# package.json

# output:
# direct-deps.txt
# reachable-deps.txt
# unused-deps.txt
# potential-deps.txt
# value_map.json

used_file_path = f'Playground/{project}/used-files.txt'
with open(used_file_path) as f:
    used_lines = f.read().splitlines()

unused_file_path = f'Playground/{project}/unused-files.txt'
with open(unused_file_path) as f:
    unused_lines = f.read().splitlines()

json_path = f'Playground/{project}/package.json'
direct_path = f'Playground/{project}/direct-deps.txt'


def get_direct_deps(json_path):
    f_package = open(json_path, encoding="utf-8")  
    packageDict = json.load(f_package)
    if "dependencies" in packageDict.keys():
        directDeps = list(packageDict['dependencies'])
        return directDeps

def get_dep_name(file_path):
    parts = file_path.rsplit("/node_modules/", 1)
    if len(parts) == 2:
        folder_name = parts[1].split("/")[0]
        return folder_name
    else:
        return None

def is_json_valid(json_path):
    if not os.path.exists(json_path):
        print(json_path + " does not exist.")
        return False
    f_package = open(json_path, encoding="utf-8")  
    packageDict = json.load(f_package)
    if "version" not in packageDict.keys():
        print(json_path + " has no version.")
        return False
    return True
    
# It is challenging to extract the root folder of the dependency to which a file belongs.
# We first find the closest node_modules to the file, if the folder under the node_modules contains
# a package.json file, then consider the folder path as the root. 
# Otherwise, check the name of the folder to see if there is an @.
# If there is, return the second level folder after the @folder.
# If there is still no package.json, check the folder under the second closest node_modules.
def extract_dep_root(file_path):
    parts = file_path.rsplit("/node_modules/", 1)

    if len(parts) != 2:
        return None
    
    first_folder = parts[1].split("/")[0]
    if "@" in first_folder:
        dep_root = parts[0] + "/node_modules/" + first_folder + "/" + parts[1].split("/")[1]
        if os.path.exists(dep_root + "/package.json"):
            return dep_root

    dep_root = parts[0] + "/node_modules/" + first_folder
    dep_root_json = dep_root + "/package.json"
    if is_json_valid(dep_root_json):
        return dep_root

    else:
        parts = file_path.rsplit("/node_modules/", 2)
        dep_name = "node_modules/" + parts[-2].split('/')[0]
        dep_root = file_path.split(dep_name)[0] + dep_name
        if is_json_valid(dep_root + "/package.json"):
            return dep_root
        else:
            parts = file_path.rsplit("/node_modules/", 3)
            print(parts)
            dep_name = "node_modules/" + parts[-3].split('/')[0]
            dep_root = file_path.split(dep_name)[0] + dep_name
            if is_json_valid(dep_root + "/package.json"):
                return dep_root

def get_dep_info(file_path):
    if not os.path.exists(file_path):
        return None
    dep_json_root = extract_dep_root(file_path)
    package_json_path = dep_json_root + "/package.json"
    print(dep_json_root)
    f_package = open(package_json_path, encoding="utf-8")  
    packageDict = json.load(f_package)
    dep_info = {}
    if "version" in packageDict.keys():
        name = packageDict.get("name")
        version = packageDict.get("version")
        dep_info["dep_version"] = version
        dep_info["dep_name"] = name
        return dep_info
    return None


direct_deps = get_direct_deps(json_path)
direct_file = open(direct_path, "a")
for item in direct_deps:
    direct_file.writelines(item + '\n')

def build_value(file_path):
    print(file_path)
    dep_info = get_dep_info(file_path)
    dep_name = dep_info["dep_name"]
    dep_root = extract_dep_root(file_path)
    dep_depth = dep_root.count("/node_modules")
    

    dep_parts = file_path.split("/node_modules/" + dep_name)
    if "/node_modules" not in dep_parts[0]:
        dep_path = "/node_modules/" + dep_name
        client_path = ""
    else:
        # Retrieve the substring before this, after the first occurrence of 'node_modules'.
        node_modules_parts = dep_parts[0].split("node_modules", 1)
        client_path = "node_modules" + node_modules_parts[1]
        dep_path = client_path + "/node_modules/" + dep_name


    if dep_name in direct_deps and client_path == "":
        is_direct = True
    else:
        is_direct = False

    value_dict = {
        "file_path": file_path,
        "dep_name": dep_info["dep_name"],
        "dep_version": dep_info["dep_version"],
        "dep_depth": dep_depth,
        "dep_path": dep_path,
        "client_path": client_path,
        "is_direct": is_direct         
    }
    return value_dict

# Generate reachable deps from used file
reachable_deps_arr = []
for path in used_lines:
    if "/node_modules/" in path:
        dep_info = get_dep_info(path)
        dep_id = dep_info["dep_name"] + "__" + dep_info["dep_version"]
        if dep_id not in reachable_deps_arr:
            reachable_deps_arr.append(dep_id)

print("There are ", len(reachable_deps_arr), "reachable dependencies in ", project)
reachable_path = f'Playground/{project}/reachable-deps.txt'
reachable_file = open(reachable_path, "a")
for item in reachable_deps_arr:
    reachable_file.writelines(item + '\n')

# Generate unreachable deps from unused file
unused_deps_arr = []
unused_file_dict_arr = []
for path in unused_lines:
    if "/node_modules/" in path:
        file_dict = build_value(path)
        unused_file_dict_arr.append(file_dict)
        dep_id = file_dict["dep_name"] + "__" + file_dict["dep_version"]
        if dep_id not in unused_deps_arr:
            unused_deps_arr.append(dep_id)

print("There are ", len(unused_deps_arr), "unused dependencies in ", project)
unused_path = f'Playground/{project}/unused-deps.txt'
unused_deps_file = open(unused_path, "a")
for item in unused_deps_arr:
    unused_deps_file.writelines(item + '\n')


# Generate potentially bloated deps from 
# the difference set of reachable deps and unreachable deps
potential_deps = list(set(unused_deps_arr).difference(reachable_deps_arr))
print("There are ", len(potential_deps), "potential bloated dependencies in ", project)
potential_path = f'Playground/{project}/potential-deps.txt'
potential_deps_file = open(potential_path, "a")
for item in potential_deps:
    potential_deps_file.writelines(item + '\n')

json_dict = {}
for item in unused_file_dict_arr:
    dep_id = item["dep_name"] + "__" + item["dep_version"]
    if dep_id in potential_deps:
        key = item["file_path"]
        json_dict[key] = item

value_map_path = f'Playground/{project}/value_map.json'

# Open the file in write mode and write the JSON data
with open(value_map_path, "w") as file:
    json.dump(json_dict, file)

# file_path = "/data/js-variants/multee/Playground/airtap/node_modules/resolve/test/resolver/symlinked/_/node_modules/foo.js"
# file_path = "/data/js-variants/multee/Playground/airtap/node_modules/browser-pack/node_modules/readable-stream/lib/internal/streams/stream.js"
# file_path = "/data/js-variants/multee/Playground/hoodie/node_modules/browser-resolve/node_modules/resolve/test/resolver/biz/node_modules/garply/lib/index.js"
# file_dict = build_value(file_path)
# print(file_dict)