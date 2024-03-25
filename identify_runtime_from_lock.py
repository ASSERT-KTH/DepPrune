import json
import os
import sys

def extract_deps(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    runtime_deps = []

    for key, value in data["packages"].items():
        # print(value.get("dev"))
        if key != "" and value.get("dev") == None:
            # package_version = value.get("version") or ""
            # package_info = f"{key}__{package_version}"
            runtime_deps.append(key)

    return runtime_deps

if __name__ == "__main__":
    project = sys.argv[1]
    folder = sys.argv[2]

    target_lock_path = os.path.abspath(f'./{folder}/{project}/package-lock.json')
    output_path = os.path.abspath(f'./{folder}/{project}/runtime_deps.txt')
    output_file = open(output_path, 'a')
    try:
        result = extract_deps(target_lock_path)

        for item in result:
            output_file.writelines(f"{item}\n")
        
    except FileNotFoundError:
        print("File not found.")
