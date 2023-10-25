import json
import os
import sys

from utils import identify_dev

if __name__ == "__main__":
    project = sys.argv[1]

    target_lock_path = os.path.abspath(f'./Playground/{project}/package-lock.json')
    output_path = f'./Playground/{project}/runtime_in_dev.txt'
    output_file = open(output_path, 'a')
    try:
        with open(target_lock_path, 'r') as file:
            json_data = json.load(file)
        
        total_deps_file = f'./Playground/{project}/total_deps_deduped.txt'
        with open(total_deps_file) as f:
            total_deps = f.read().splitlines()
        
        for dep in total_deps:
            deparr = dep.split('__')
            target_dep = deparr[0]
            target_version = deparr[1]
            dev_deps = identify_dev(json_data, target_dep, target_version)
            if dev_deps:
                print(dep, " found in dev")
                output_file.writelines(f"{dep}\n")
        
    except FileNotFoundError:
        print("File not found.")
