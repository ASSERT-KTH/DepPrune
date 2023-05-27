import requests

headers = {
    "Authorization": "Bearer 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"
}

filePath = f'./Logs/repo_commited_in_2023.txt'
with open(filePath) as f:
    lines = f.read().splitlines()

def get_default_branch(repoinfo):
    url = f"https://api.github.com/repos/{repoinfo}"
    response = requests.get(url, headers = headers)
    
    if response.status_code == 200:
        repository = response.json()
        default_branch = repository["default_branch"]
        return default_branch
    else:
        response.raise_for_status() 


new_lines = []
for item in lines:
    line = item.split(',')
    repoinfo = line[1]
    print(repoinfo)
    default_branch = get_default_branch(repoinfo)
    new_item = f'{line[0]},{default_branch},{repoinfo},{line[2]}\n'
    print(new_item)
    new_lines.append(new_item)

with open(filePath, "w") as file:
    file.writelines(new_lines)
