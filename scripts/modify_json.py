import json

file_path = f"./Playground/lad/value_map.json"

with open(file_path, 'r') as file:
    data = json.load(file)

# Modify the data
for key, value in data.items():
    if value.get("dep_name") == "semver" and value.get("dep_version") == "7.3.7":
        print(1)
        value["is_direct"] = False

with open(file_path, 'w') as file:
    json.dump(data, file, indent=2)