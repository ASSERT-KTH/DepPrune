filePath = f'./Logs/repo_commited_in_2023_entry.txt'
with open(filePath) as f:
    lines = f.read().splitlines()

entry_raw_filePath = f'./Logs/repo_commited_in_2023_entry_raw.txt'


def generate_raw_github_url(repository, branch, file_path):
    base_url = "https://raw.githubusercontent.com"
    file_path = file_path.lstrip("./")
    url = f"{base_url}/{repository}/{branch}/{file_path}"
    return url

entry_raw_file = open(entry_raw_filePath, 'a')
for item in lines:
    line = item.split(',')
    repo = line[0]
    branch = line[1]
    raw_url = line[2]
    raw_github_url = generate_raw_github_url(repo, branch, raw_url)
    entry_raw_file.writelines(repo + ',' + branch + ',' + raw_github_url + '\n')