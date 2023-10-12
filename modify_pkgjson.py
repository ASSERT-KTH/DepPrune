import json
import sys
project = sys.argv[1]

json_path = f"../../DebloatedPackages/{project}/package.json"
deps_path = f"../../Playground/{project}/direct_confirmed_deps.txt"
direct_deps = []

with open(json_path, 'r') as file:
    data = json.load(file)

with open(deps_path) as f:
    deps = f.read().splitlines()

for dep in deps:
    name = dep.split("__")[0]
    direct_deps.append(name)

print(direct_deps)
for package in direct_deps:
    if package in data.get('dependencies', {}) and package not in data.get('bundleDependencies', []):
        del data['dependencies'][package]

with open(json_path, 'w') as file:
    json.dump(data, file, indent=2)