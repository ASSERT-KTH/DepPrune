import json

# Assuming 'data.json' contains your JSON data
with open('repos_93.json', 'r') as json_file:
    data = json.load(json_file)
projects_93 = data["projects"]

direct_file = f'./repos_44.txt'
with open(direct_file) as f:
    projects_to_filter = f.read().splitlines()

# Filter items where the 'project' key matches the values in the projects_to_filter list
filtered_projects = [item for item in projects_93 if item.get('folder') in projects_to_filter]

filtered_data = {
    "projects": filtered_projects
}
# Save the filtered data back to a JSON file or use it as needed
with open('repos_44.json', 'w') as filtered_file:
    json.dump(filtered_data, filtered_file, indent=4)

