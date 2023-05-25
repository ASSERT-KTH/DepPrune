import requests
import pandas as pd

# Assuming you have a CSV file called 'data.csv' with a column named 'column_name'

df = pd.read_csv('./Csvs/2707-deduplicated.csv')
repo_values = df['URL'].tolist()


def get_last_commit(repoinfo):
    url = f"https://api.github.com/repos/{repoinfo}/commits"
    response = requests.get(url)
    
    if response.status_code == 200:
        commits = response.json()
        if len(commits) > 0:
            last_commit = commits[0]['commit']['committer']['date'][:4]
            return last_commit
        else:
            return None  # No commits in the repository
    elif response.status_code == 404 or response.status_code == 403:
        return "404 or 403"
    else:
        response.raise_for_status()  # Raise an exception for other status codes
        


for item in repo_values:
    last_commit = get_last_commit(item)
    if last_commit is not None:
        print("Last Commit:", last_commit)
    elif last_commit == "404 or 403":
        print("404 or 403")
    else:
        print("No commits found in the repository.")