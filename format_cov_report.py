import json
import sys
project = sys.argv[1]

file_path = f'Playground/{project}/coverage/coverage-final.json'
with open(file_path, 'r') as json_file:
    data = json.load(json_file)

with open(file_path, 'w') as json_file:
    json.dump(data, json_file, indent=2)

print(project, 'JSON file formatted successfully.')
