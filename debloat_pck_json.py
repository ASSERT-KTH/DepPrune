import json
import os
import sys

def remove_directs(json_obj, directs):
    for direct in directs:
        name = reg_names(direct)["dep"]
        del json_obj["dependencies"][name]
    return json_obj

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

    target_path = os.path.abspath(f'./DebloatedLocks/{project}/package.json')
    print(target_path)
    try:
        with open(target_path, 'r') as file:
            json_data = json.load(file)

        direct_bloated_file = os.path.abspath(f'./Playground/{project}/direct_bloated.txt')
        if os.path.getsize(direct_bloated_file) != 0:
            with open(direct_bloated_file) as f:
                confirmed_directs = f.read().splitlines()
            remove_directs(json_data, confirmed_directs)
        
        with open(target_path, 'w') as file:
            json.dump(json_data, file, indent=4)

    except FileNotFoundError:
        print("File not found.")
