import requests

# Assuming you have a CSV file called 'data.csv' with a column named 'column_name'

headers = {
    "Authorization": "Bearer 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"
}

def get_commit_status(repoinfo):
    url = f"https://api.github.com/repos/{repoinfo}/commits"
    params = {'per_page': 100}  # Set the number of commits per page
    commit_count = 0
    page = 1

    while True:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            commit_count += len(data)
            if len(data) < 100:
                break  # Reached the last page
            else:
                page += 1
                params['page'] = page
        else:
            return -1  # Indicates an error occurred

    return commit_count    

filePath = f'./Logs/repo_NodeJS_100000_rest.txt'
with open(filePath) as f:
    repo_NodeJS_100000 = f.read().splitlines()

filePath_commits = f'./Logs/repo_NodeJS_100000_commits.txt'
file_commits = open(filePath_commits, "a")

for line in repo_NodeJS_100000:
    item = line.split(',')
    repoinfo = item[1]

    commit_count = get_commit_status(repoinfo)
    if commit_count == -1:
        break
    item[3] = commit_count
    print(repoinfo)
    new_line = ",".join(str(v) for v in item) + "\n"
    file_commits.writelines(new_line)




