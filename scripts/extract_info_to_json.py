import urllib.parse

import json

txt_file = f'Logs/target_103_loc.txt'
json_file = 'repos.json'

data = {}
data['projects'] = []

with open(txt_file, 'r') as file:
    lines = file.readlines()

for line in lines:
    items = line.split(',')
    folder = items[0]
    repo = items[1]
    sha = items[7]
    entry_url = items[9]
    giturl = items[10].strip()

    entry_url_temp = urllib.parse.urlparse(entry_url)
    entry = entry_url_temp.path.lstrip("/")
    specific_entry = "/".join(entry.split("/")[3:])
    print(specific_entry)
    temp_dict = {
        'folder': folder,
        'repo': repo,
        'commit': sha,
        'entryFile': specific_entry,
        'gitURL': giturl
    }
    data['projects'].append(temp_dict)

with open(json_file, 'w') as file:
    json.dump(data, file, indent=2)

print("Data has been successfully converted to JSON format and saved to the output file.")
