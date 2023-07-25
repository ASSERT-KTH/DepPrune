
import sys
import json
import os

project = sys.argv[1]

potential_deps_path = f'./Playground/{project}/potential-deps.txt'
if os.path.exists(potential_deps_path):
    with open(potential_deps_path) as f:
        potential_deps = f.read().splitlines()
    print(len(potential_deps))
else:
    sys.exit()

direct_deps_path = f'./Playground/{project}/direct-deps.txt'
with open(direct_deps_path) as f:
    direct_deps = f.read().splitlines()
print(len(direct_deps))

json_path = f'./Playground/{project}/value_map.json'
f_package = open(json_path, encoding="utf-8")  
deps_dict = json.load(f_package)


# intersection = [arr1 for arr1 in list1 for arr2 in list2 if arr1[0] == arr2[0]]
direct_bloated = list(set(potential_deps).intersection(direct_deps))

print(direct_bloated)

# difference = list(set(lines1).difference(lines2))
# print(len(difference))


direct_bloated_file = open(f'./Playground/{project}/bloated_direct_deps.txt', "a")
for item in direct_bloated:
    direct_bloated_file.writelines(item+ "\n")
    