import json
import sys
project = sys.argv[1]

file_path = f'Playground/{project}/coverage/coverage-final.json'
# Load the JSON file
with open(file_path, 'r') as json_file:
    data = json.load(json_file)

# Dump the formatted JSON data back to the file with an indentation of 2 spaces
with open(file_path, 'w') as json_file:
    json.dump(data, json_file, indent=2)

print(project, 'JSON file formatted successfully.')
