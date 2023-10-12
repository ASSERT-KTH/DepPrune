import sys
import os
import json

project = sys.argv[1]

reachable_file_path = f'Playground/{project}/reachable_files.txt'
with open(reachable_file_path) as f:
    reachable_files = f.read().splitlines()


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




# Generate reachable deps from used file
reachable_deps_arr = []
for path in reachable_files:
    if "/node_modules/" in path:
        dep_info = get_dep_info(path)
        dep_id = dep_info["dep_name"] + "__" + dep_info["dep_version"]
        if dep_id not in reachable_deps_arr:
            reachable_deps_arr.append(dep_id)

print("There are ", len(reachable_deps_arr), "reachable dependencies in ", project)
reachable_deps_path = f'Playground/{project}/reachable_deps.txt'
reachable_file = open(reachable_deps_path, "a")
for item in reachable_deps_arr:
    reachable_file.writelines(item + '\n')