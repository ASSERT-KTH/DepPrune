import json
import sys

filename = sys.argv[1]
depname = sys.argv[2]

def remove_dependency(package_file, dependency_name):
    with open(package_file, "r") as file:
        data = json.load(file)  # Parse the package.json file as JSON

    if "dependencies" in data and dependency_name in data["dependencies"]:
        del data["dependencies"][dependency_name]  # Remove the desired dependency

    if "devDependencies" in data and dependency_name in data["devDependencies"]:
        del data["devDependencies"][dependency_name]  # Remove the desired devDependency

    with open(package_file, "w") as file:
        json.dump(data, file, indent=4)  # Write the updated JSON back to the package.json file

remove_dependency(filename, depname)
