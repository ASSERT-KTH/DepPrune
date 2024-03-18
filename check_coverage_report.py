import json

def collect_keys_with_string(input_file, output_file, search_string):
    collected_data = {}

    with open(input_file, 'r') as f:
        data = json.load(f)

    # Create a copy of keys before iterating
    keys_to_modify = list(data.keys())

    # Iterate over the copied keys
    for key in keys_to_modify:
        if search_string in key:
            collected_data[key] = data[key]

    with open(output_file, 'w') as f:
        json.dump(collected_data, f, indent=4)

input_file = 'stubbifier/Playground/kuzzle-plugin-mqtt/coverage/coverage-final.json'
output_file = 'collected_data.json'
search_string = 'node_modules/estraverse'

collect_keys_with_string(input_file, output_file, search_string)
