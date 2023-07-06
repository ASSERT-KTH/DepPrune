
import sys
import json

project = sys.argv[1]

direct_deps_path = f'./Playground/{project}/direct-deps.txt'
with open(direct_deps_path) as f:
    direct_deps = f.read().splitlines()
print(len(direct_deps))

potential_deps_path = f'./Playground/{project}/potential-deps.txt'
with open(potential_deps_path) as f:
    potential_deps = f.read().splitlines()
print(len(potential_deps))


json_path = f'./Playground/{project}/bloated_deps_physical_level.json'
f_package = open(json_path, encoding="utf-8")  
deps_dict = json.load(f_package)

multiple_deps = []

for dep in deps_dict:
    print(deps_dict[dep])
    if len(deps_dict[dep]['level']) > 1:
        multiple_deps.append(deps_dict[dep]['name'])
print(len(multiple_deps))

multiple_bloated = list(set(multiple_deps).intersection(potential_deps))
direct_bloated = list(set(potential_deps).intersection(direct_deps))

print(multiple_bloated)
print(direct_bloated)

# difference = list(set(lines1).difference(lines2))
# print(len(difference))
multiple_bloated_file = open(f'./Playground/{project}/bloated_multiple_deps.txt', "a")
for item in multiple_bloated:
    multiple_bloated_file.writelines(item+ "\n")

direct_bloated_file = open(f'./Playground/{project}/bloated_direct_deps.txt', "a")
for item in direct_bloated:
    direct_bloated_file.writelines(item+ "\n")
    