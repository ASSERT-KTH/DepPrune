import json

def get_direct_deps(json_path):
    f_package = open(json_path, encoding="utf-8")  
    pck_dict = json.load(f_package)
    if "dependencies" in pck_dict.keys():
        direct_deps = list(pck_dict['dependencies'])
        return direct_deps

def get_dep_version(name, project):
    json_path = f'Playground/{project}/node_modules/{name}/package.json'
    f_package = open(json_path, encoding="utf-8")  
    pck_dict = json.load(f_package)
    if "version" in pck_dict.keys():
        return pck_dict.get("version")

def find_keys_with_version(json_data, target_dep, target_version, key_prefix=""):
    keys_with_version = []
    for key, value in json_data.items():
        if key.endswith("/" + target_dep) and isinstance(value, dict) and value.get("version") == target_version:
            full_key_name = f"{key_prefix}/{key}" if key_prefix else key
            keys_with_version.append(full_key_name)
        elif isinstance(value, dict):
            keys_with_version.extend(find_keys_with_version(value, target_version, key))
    return keys_with_version

def find_keys_with_root_dependency(json_obj, target_dependency, parent_keys=[]):
    matching_keys = []
    if isinstance(json_obj, dict):
        if "dependencies" in json_obj and "dev" not in json_obj and target_dependency in json_obj["dependencies"]:
            matching_keys.append(".".join(parent_keys[1:]))

        for key, value in json_obj.items():
            matching_keys.extend(find_keys_with_root_dependency(value, target_dependency, parent_keys + [key]))
    elif isinstance(json_obj, list):
        for index, item in enumerate(json_obj):
            matching_keys.extend(find_keys_with_root_dependency(item, target_dependency, parent_keys + [str(index)]))

    return matching_keys

def transform_string_to_array(input_string, substring):
    parts = input_string.split(substring)
    result = [substring + part[:-1] if '/' in part else substring + part for part in parts if part]
    return result

def transform_array_with_string(input_array, join_string):
    output_array = []
    current_path = ""

    for item in input_array:
        if current_path:
            current_path += "/"
        current_path += item
        output_array.append(current_path + "/" + join_string)

    return output_array

def is_key_contains_the_version(json_data, key, target_dep):
    is_removing = True
    temp_arr = transform_string_to_array(key, "node_modules/")
    output_arr = transform_array_with_string(temp_arr, f"node_modules/{target_dep}")
    for item in output_arr:
        if item in json_data["packages"]:
            is_removing = False

    return is_removing

def remove_dependency(json_obj, package_name, dependency_name):
    if package_name in json_obj["packages"] and "dependencies" in json_obj["packages"][package_name] and "dev" not in json_obj["packages"][package_name]:
        dependencies = json_obj["packages"][package_name]["dependencies"]
        if dependency_name in dependencies:
            del dependencies[dependency_name]
    return json_obj

def get_substring_before_last_node_modules(input_string):
    # Find the last occurrence of "/node_modules/"
    last_occurrence = input_string.rfind("node_modules/")

    # Check if "/node_modules/" was found in the string
    if last_occurrence != -1:
        # Extract the substring before the last occurrence
        substring = input_string[:last_occurrence + len("node_modules/")]
        return substring

def remove_from_lock(json_data, target_dep, target_version):
    parent_deps = []  
    matching_target_keys = find_keys_with_version(json_data["packages"], target_dep, target_version)
    # print("matching_target_keys", matching_target_keys)

    for matching_key in matching_target_keys:
        # substr =  get_substring_before_last_node_modules(matching_key)
        # print(substr)
        # only dependencies within the same node_modules where the target dependency is in, can depends on the target dependency
        # For example: only node_modules/a or node_modules/a/node_modules/b or node_modules/a/node_modules/b/node_modules/c can depend on node_modules/e
        parent_pre = matching_key[:-len("node_modules/" + target_dep)]
        print("parent_pre", parent_pre)
        matching_parent_keys = find_keys_with_root_dependency(json_data["packages"], target_dep, [parent_pre])


        if parent_pre == "":
            # Target dependency is in the root of /node_modules, it is a direct dependency or is depended by some other dependency in the root of /node_modules
            for potential_parent_key in matching_parent_keys:
                if is_key_contains_the_version(json_data, potential_parent_key, target_dep):
                    print("1. key: " + potential_parent_key)
                    parent_deps.append(potential_parent_key)
                    remove_dependency(json_data, potential_parent_key, target_dep)
        
                                
        elif parent_pre != "":
            # Target dependency is not in the root of node_modules    
            # Check from the folder of node_modules/parent
            # Plus, check from the folder of node_modules/parent/node_modules/other_packages
            # For example, for "node_modules/read-pkg/node_modules/parse-json", the parent_key is "node_modules/read-pkg"
            # check in "node_modules/read-pkg" and check in "node_modules/read-pkg/node_modules/any_other"
            # matching_keys = find_keys_with_root_dependency(json_data["packages"], target_dep, [potential_parent_key])
            # print("matching_keys", matching_keys)
            
            filtered_keys = [item for item in matching_parent_keys if item.startswith(parent_pre[:-1])]
            if filtered_keys:
                for key in filtered_keys:
                    extra_version_path = f"{key}/node_modules/{target_dep}"
                    if extra_version_path in json_data["packages"] and key + "/" == parent_pre:
                        print("2. key: " + key)
                        parent_deps.append(key)
                        remove_dependency(json_data, key, target_dep)
                    if extra_version_path not in json_data["packages"]:
                        print("3. key: " + key)
                        parent_deps.append(key)
                        remove_dependency(json_data, key, target_dep)
        else:
            print(f"No keys found with dependency '{target_dep}'.")
    print(parent_deps)

def identify_dev(json_data, target_dep, target_version):
    # Identify a dependency that are not able to debloat, still in the debloated lock file.
    # indicating the dependency is used in "dev":true dependencies.
    dep_in_dev = False  
    matching_target_keys = find_keys_with_version(json_data["packages"], target_dep, target_version)
    print("matching_target_keys", target_dep, target_version, matching_target_keys)

    if (len(matching_target_keys) != 0):
        dep_in_dev = True
        
    return dep_in_dev