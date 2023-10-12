import json

# Function to read and process the JSON file
def process_json_file(json_file):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)

        # Extract project information and format it
        result = [
            f"{project['folder']},{project['coverage'].split(' | ')[0]}"
            for project in data.get('projects', [])
        ]

        return result

    except FileNotFoundError:
        return []

# Provide the path to your JSON file
json_file_path = 'repos_98_test_copy.json'  # Replace with your file path

# Process the JSON file and get the result
output_list = process_json_file(json_file_path)

# Print the result
for item in output_list:
    print(item)
