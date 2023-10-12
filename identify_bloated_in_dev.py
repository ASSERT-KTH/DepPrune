import json
import os
import sys

from utils import identify_dev

if __name__ == "__main__":
    project = sys.argv[1]
    # parent_dev_deps = []

    target_lock_path = os.path.abspath(f'./DebloatedPackages/{project}/package-lock.json')
    output_path = f'./Playground/{project}/indirect_pseudo_bloated_deps.txt'
    output_file = open(output_path, 'a')
    try:
        with open(target_lock_path, 'r') as file:
            json_data = json.load(file)
        
        confirm_bloated_file = f'./Playground/{project}/individual_confirmed_deps.txt'
        with open(confirm_bloated_file) as f:
            confirmed_deps = f.read().splitlines()
        
        for dep in confirmed_deps:
            # print("removing dependency: ", dep)
            deparr = dep.split('__')
            target_dep = deparr[0]
            target_version = deparr[1]
            dev_deps = identify_dev(json_data, target_dep, target_version)
            if dev_deps:
                # parent_dev_deps.extend(dev_deps)
                output_file.writelines(f"{project}, {dep}, {str(dev_deps)}\n")
        
        # print(parent_dev_deps)
        # output_file.writelines(f"{project},{len(parent_dev_deps)}\n")
    except FileNotFoundError:
        print("File not found.")
