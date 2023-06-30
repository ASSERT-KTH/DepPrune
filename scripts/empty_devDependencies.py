import json
import sys

folder = sys.argv[1]

# Specify the path to your package.json file
package_json_path = f'Original/{folder}/package.json'

# Read the contents of the package.json file
with open(package_json_path, 'r') as file:
    data = json.load(file)

# Empty the devDependencies object
data['devDependencies'] = {}

# Write the updated contents back to the package.json file
with open(package_json_path, 'w') as file:
    json.dump(data, file, indent=2)

print("devDependencies in " + folder + " package.json have been emptied.")