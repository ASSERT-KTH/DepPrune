import requests

filePath = f'./Logs/repo_100000_entry_raw.txt'
with open(filePath) as f:
    lines = f.read().splitlines()

entry_filePath = f'./Logs/repo_100000_valid_entry.txt'
entry_file = open(entry_filePath, 'a')

entry_file_errorPath = f'./Logs/repo_100000_valid_entry_error.txt'
entry_file_error = open(entry_file_errorPath, 'a')

def request_raw_url(repo, raw_file_url):

    # Make the HTTP GET request
    url = f'{raw_file_url}'
    response = requests.get(url)
    if response.status_code == 200:
        entry_file.writelines(repo + ',' + raw_file_url + '\n')
    
    else:
        print("Failed to retrieve the file. Status code:", response.status_code)
        entry_file_error.writelines(repo + ',' + raw_file_url + ',' + str(response.status_code) + '\n')

for item in lines:
    line = item.split(',')
    repo = line[0]
    raw_url = line[2]
    print(repo, raw_url)
    if "dist/" not in raw_url:
        request_raw_url(repo, raw_url)