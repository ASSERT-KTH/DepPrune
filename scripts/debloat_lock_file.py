import json
import os
import sys

def remove_directs(json_obj, directs):
    for direct in directs:
        name = reg_names(direct)["dep"]
        del json_obj["packages"][""]["dependencies"][name]
    return json_obj

def remove_indirect(json_obj, key):
    # remove each occurance from the runtime deps that specify the corresponding dependency, the deps can be each dep where its path starts with the same node_modules folder
    dep_obj = reg_names(key)
    folder = dep_obj["folder"]
    name = dep_obj["dep"]
    print("folder", folder)
    print("name", name)
    used_in_dev = False

    prefix = ""
    if folder == "":
        prefix = "node_modules/"
    else:
        prefix = f'{folder}/node_modules/'
     
    keys_matching = collect_keys(json_obj["packages"], prefix, name)

    for match_key in keys_matching:
        if "dependencies" in json_obj["packages"][match_key] and name in json_obj["packages"][match_key]["dependencies"] and "dev" in json_obj["packages"][match_key]:
            used_in_dev = True
            print("matching in dev: ", match_key)
        if "dependencies" in json_obj["packages"][match_key] and name in json_obj["packages"][match_key]["dependencies"] and "dev" not in json_obj["packages"][match_key]:
            print("matching: ", match_key)
            # remove the key from the object
            del json_obj["packages"][match_key]["dependencies"][name]
    
    # if json_obj["packages"][folder] and json_obj["packages"][folder]["dependencies"] and name in json_obj["packages"][folder]["dependencies"]:
    #     del json_obj["packages"][folder]["dependencies"][name]
    if not used_in_dev:
        del json_obj["packages"][key]
    else:
        json_obj["packages"][key]["dev"] = True
    # del json_obj["packages"][key]

    return json_obj

def collect_keys(json_obj, prefix, name):
    keys_matching = []
    for key in json_obj.keys():
        if key.startswith(prefix):
            key_without_prefix = key[len(prefix):]
            sub_dep = "node_modules/" + name
            if sub_dep not in key_without_prefix:
                keys_matching.append(key)
    return keys_matching


def reg_names(input_string):
    parts = input_string.rsplit("node_modules", 1)
    if len(parts) == 2:
        return {
            "folder": parts[0].strip("/"),
            "dep": parts[1].strip("/")
        }
    else:
        return {
            "folder": "",
            "dep": parts[0].strip("/")
        }

    


if __name__ == "__main__":
    project = sys.argv[1]

    target_lock_path = os.path.abspath(f'./DebloatedLocks/{project}/package-lock.json')
    try:
        with open(target_lock_path, 'r') as file:
            json_data = json.load(file)

        direct_bloated_file = os.path.abspath(f'./Playground/{project}/direct_bloated.txt')
        if os.path.getsize(direct_bloated_file) != 0:
            with open(direct_bloated_file) as f:
                confirmed_directs = f.read().splitlines()
            remove_directs(json_data, confirmed_directs)

        confirm_bloated_file = f'./Playground/{project}/unreachable_runtime_deps_removed.txt'
        with open(confirm_bloated_file) as f:
            confirmed_deps = f.read().splitlines()
        
        for dep in confirmed_deps:
            remove_indirect(json_data, dep)

        # confirm_bloated_file = f'./Playground/{project}/unreachable_runtime_deps_removed.txt'
        # with open(confirm_bloated_file) as f:
        #     confirmed_deps = f.read().splitlines()
        
        for dep in confirmed_deps:
            remove_indirect(json_data, dep)
        
        with open(target_lock_path, 'w') as file:
            json.dump(json_data, file, indent=4)

    except FileNotFoundError:
        print("File not found.")
