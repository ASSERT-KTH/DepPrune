import requests

filePath = f'./Logs/repo_commited_in_2023_entry_raw.txt'
with open(filePath) as f:
    lines = f.read().splitlines()

entry_filePath = f'./Logs/repo_commited_in_2023_valid_entry.txt'
entry_file = open(entry_filePath, 'a')

def request_raw_url(repo, raw_file_url):

    # Make the HTTP GET request
    url = f'{raw_file_url}'
    response = requests.get(url)
    if response.status_code == 200:
        entry_file.writelines(repo + ',' + raw_file_url + '\n')
    
    else:
        print("Failed to retrieve the file. Status code:", response.status_code)

for item in lines:
    line = item.split(',')
    repo = line[0]
    raw_url = line[2]
    request_raw_url(repo, raw_url)