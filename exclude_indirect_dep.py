import json
import os
import sys

from utils import remove_from_lock

if __name__ == "__main__":
    target_dep = sys.argv[1]
    target_version = sys.argv[2]
    project = sys.argv[3]
    TestFolder = "TestCollection"

    target_lock_path = os.path.abspath(f'../../{TestFolder}/{project}/package-lock.json')

    try:
        with open(target_lock_path, 'r') as file:
            json_data = json.load(file)

        # Find the location of the dependency with the specific version, and get the parant dependency
        remove_from_lock(json_data, target_dep, target_version)
        
        with open(target_lock_path, 'w') as file:
            json.dump(json_data, file, indent=4)
    except FileNotFoundError:
        print("File not found.")
