import sys
import json
project = sys.argv[1]


unused_file_path = f'Playground/{project}/unused-files.txt'
with open(unused_file_path) as f:
    unused_lines = f.read().splitlines()

dependencies = []
level_dict = {}

def find_dependency_levels(path):
    
    parts = path.split("/node_modules/")
    
    for i, dep_name in enumerate(parts[1:], start=1):
        dependency_name = dep_name.split("/")[0]
        level = i

        dependency = {
            "dependency_name": dependency_name,
            "level": level
        }
        dependencies.append(dependency)

        if dependency_name not in level_dict:
            level_dict[dependency_name] = {
                "name": dependency_name,
                "level": []
            }
        if level not in level_dict[dependency_name]["level"]:
            level_dict[dependency_name]["level"].append(level)

for path in unused_lines:
    find_dependency_levels(path)

level_path = f'Playground/{project}/bloated_deps_physical_level.txt'
level_file = open(level_path, "a")
for item in dependencies:
    text = f'{item["dependency_name"]},{item["level"]}\n'
    level_file.writelines(text)

json_path = f'Playground/{project}/bloated_deps_physical_level.json'
with open(json_path, "w") as file:
    json.dump(level_dict, file, indent=4)
