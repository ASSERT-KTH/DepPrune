import os
import json
import sys

project = sys.argv[1]

def get_package_version(package_json_path):
    if os.path.exists(package_json_path):
        with open(package_json_path, "r") as f:
            try:
                package_data = json.load(f)
                return package_data.get("version", None)
            except json.JSONDecodeError:
                return None

def get_versions_in_node_modules(root_path):
    versions = {}
    
    for root, dirs, files in os.walk(root_path):
        if "node_modules" in dirs:
            node_modules_path = os.path.join(root, "node_modules")
            for package_dir in dirs:
                package_json_path = os.path.join(node_modules_path, package_dir, "package.json")
                version = get_package_version(package_json_path)
                
                if version:
                    versions[package_dir] = version
                
    return versions

root_path = f"./Playground/{project}"
dependencies = get_versions_in_node_modules(root_path)
print(dependencies)

for package_name, version in dependencies.items():
    print(f"{package_name}: {version}")
