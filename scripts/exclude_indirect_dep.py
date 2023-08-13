import json
import os
import sys

def find_key_with_version(json_data, target_dep, target_version, key_prefix=""):
    for key, value in json_data.items():
        if key.endswith("/" + target_dep) and isinstance(value, dict) and value.get("version") == target_version:
            full_key_name = key
            return full_key_name
        elif isinstance(value, dict):
            found_key = find_key_with_version(value, target_dep, target_version, key)
            if found_key:
                return found_key
    return None

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
    # print(parent_keys)
    matching_keys = []
    if isinstance(json_obj, dict):
        # print(parent_keys)
        if "dependencies" in json_obj and target_dependency in json_obj["dependencies"]:
            matching_keys.append(".".join(parent_keys[1:]))
            # matching_keys.append(parent_keys[1:])

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

def is_key_contains_the_unroot_version(json_data, key, target_dep):
    is_removing = True
    temp_arr = transform_string_to_array(key)
    # Todo: only consider if current key + "node_modules/{target_dep}" or further has another version
    output_arr = transform_array_with_string(temp_arr, f"node_modules/{target_dep}")
    for item in output_arr:
        if item in json_data["packages"]:
            print(key + " has another version of the dependency " + target_dep)
            is_removing = False
        else:
            print(key + " has the version of the dependency " + target_dep)
    return is_removing

def remove_dependency(json_obj, package_name, dependency_name):
    if package_name in json_obj["packages"] and "dependencies" in json_obj["packages"][package_name]:
        dependencies = json_obj["packages"][package_name]["dependencies"]
        if dependency_name in dependencies:
            del dependencies[dependency_name]

if __name__ == "__main__":
    # file_path = f"../aliv/package-lock.json"
    # target_version = "2.81.0"
    # target_dep = "request"
    target_dep = sys.argv[1]
    target_version = sys.argv[2]
    input_path = sys.argv[3]

    file_path = os.path.abspath(input_path)
    # target_version = "3.1.1"
    # target_dep = "readable-stream"

    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)

        # Find the location of the dependency with the specific version, and get the parant depend
        matching_keys = find_keys_with_version(json_data["packages"], target_dep, target_version)
        print(matching_keys)
        # matching_key = find_key_with_version(json_data["packages"], target_dep, target_version)
        for matching_key in matching_keys:
            substring = "node_modules/" + target_dep
            parent_key = matching_key[:-len(substring)]
            print("parent_key: " + parent_key)
            if matching_key:
                print(f"Key ending with '{target_dep}' and version '{target_version}':")
                print("matching_key: " + matching_key)
            else:
                print(f"No key found with version '{target_version}' and ending with '{target_dep}'.")

            if parent_key == "":
                # Target dependency is in the root of /node_modules, it is a direct dependency or is depended by some other dependency in the root of /node_modules
                matching_keys = find_keys_with_root_dependency(json_data["packages"], target_dep, [parent_key])
                if matching_keys:
                    for key in matching_keys:
                        if is_key_contains_the_version(json_data, key, target_dep):
                            print("1. key: " + key)
                            # remove_dependency(json_data, key, target_dep)    
            elif parent_key != "":
                # Target dependency is not in the root of node_modules    
                # Check from the folder of node_modules/parent_key
                matching_keys = find_keys_with_root_dependency(json_data["packages"], target_dep, [parent_key])
                filtered_keys = [item for item in matching_keys if parent_key in item]
                if filtered_keys:
                    for key in filtered_keys:
                        extra_version_path = f"{key}/node_modules/{target_dep}"
                        if extra_version_path not in json_data["packages"]:
                            print("2. key: " + key)
                            # remove_dependency(json_data, key, target_dep)

                print("3. key: " + parent_key[:-1])
                # remove_dependency(json_data, parent_key[:-1], target_dep)
            else:
                print(f"No keys found with dependency '{target_dep}'.")

        with open(file_path, 'w') as file:
            json.dump(json_data, file, indent=4)
    except FileNotFoundError:
        print("File not found.")
