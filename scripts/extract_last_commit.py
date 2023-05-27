import requests
import pandas as pd

# Assuming you have a CSV file called 'data.csv' with a column named 'column_name'

df = pd.read_csv('./Csvs/2379-2707-deduplicated.csv')
repo_values = df.values.tolist()

headers = {
    "Authorization": "Bearer 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"
}

def get_last_commit(repoinfo):
    url = f"https://api.github.com/repos/{repoinfo}/commits"
    response = requests.get(url, headers = headers)
    
    if response.status_code == 200:
        commits = response.json()
        if len(commits) > 0:
            last_commit = commits[0]['commit']['committer']['date'][:4]
            return last_commit
        else:
            return None  # No commits in the repository
    elif response.status_code == 404:
        return "404"
    elif response.status_code == 409:
        return "409"
    
    elif response.status_code == 403 and "rate limit" in response.text.lower():
        raise RateLimitException("Rate limit exceeded. Retrying...")
    else:
        response.raise_for_status()  # Raise an exception for other status codes

class RateLimitException(Exception):
    pass       

try:
    file_commit2023 = open("Logs/repo_commited_in_2023.txt", "w")
    file_commit2023_errors = open("Logs/repo_commited_in_2023_errors.txt", "w")
    for item in repo_values:
        repoinfo = item[2]

        last_commit = get_last_commit(repoinfo)

        if last_commit is not None and last_commit == "2023":
            text = f'{item[0]},{repoinfo},{item[3]}\n'
            print(text)
            file_commit2023.writelines(text)

        elif last_commit == "404":
            print(item[0], "404")
            text = f'{item[0]},{repoinfo}, 404\n'
            file_commit2023_errors.writelines(text)

        elif last_commit == "409":
            text = f'{item[0]},{repoinfo}, 409 empty\n'
            file_commit2023_errors.writelines(text)
            print(item[0], "409 empty")

        else:
            text = f'{item[0]},{repoinfo}, not in 2023\n'
            file_commit2023_errors.writelines(text)
            print("not in 2023")

except RateLimitException:
    print("Rate limit exceeded. Please try again later.")

