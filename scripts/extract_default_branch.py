import requests

headers = {
    "Authorization": "Bearer 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"
}

# filePath = f'./Logs/repo_commited_in_2023.txt'
filePath = f'./Logs/repo_commited_in_2023_100000.txt'
with open(filePath) as f:
    lines = f.read().splitlines()

filePath_branch = f'./Logs/repo_commited_in_2023_100000_branch.txt'

def get_default_branch(repoinfo):
    url = f"https://api.github.com/repos/{repoinfo}"
    response = requests.get(url, headers = headers)
    
    if response.status_code == 200:
        repository = response.json()
        default_branch = repository["default_branch"]
        return default_branch
    else:
        return response.raise_for_status() 


file_branch = open(filePath_branch, "a")
for item in lines:
    line = item.split(',')
    repoinfo = line[1]
    print(repoinfo)
    default_branch = get_default_branch(repoinfo)
    new_item = f'{line[0]},{default_branch},{repoinfo},{line[2]}\n'
    file_branch.writelines(new_item)
