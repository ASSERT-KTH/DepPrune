import json
import os
import sys

from utils import remove_from_lock

if __name__ == "__main__":
    project = sys.argv[1]

    target_lock_path = os.path.abspath(f'../../DebloatedPackages/{project}/package-lock.json')
    try:
        with open(target_lock_path, 'r') as file:
            json_data = json.load(file)
        
        confirm_bloated_file = f'../../Playground/{project}/individual_confirmed_deps.txt'
        with open(confirm_bloated_file) as f:
            confirmed_deps = f.read().splitlines()

        print("confirmed_deps", confirmed_deps)
        
        for dep in confirmed_deps:
            print("removing dependency: ", dep)
            deparr = dep.split('__')
            target_dep = deparr[0]
            target_version = deparr[1]
            remove_from_lock(json_data, target_dep, target_version)
        
        with open(target_lock_path, 'w') as file:
            json.dump(json_data, file, indent=4)
    except FileNotFoundError:
        print("File not found.")
