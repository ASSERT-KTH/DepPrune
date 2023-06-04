import requests
import pandas as pd

# Assuming you have a CSV file called 'data.csv' with a column named 'column_name'

# df = pd.read_csv('./Csvs/2379-2707-deduplicated.csv')
df = pd.read_csv('./Csvs/40039-35321-deduplicated-rest.csv')
# df = pd.read_csv('./Csvs/test.csv')
repo_values = df.values.tolist()

headers = {
    "Authorization": "Bearer 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"
}

def get_commit_status(repoinfo):
    url = f"https://api.github.com/repos/{repoinfo}/commits"
    response = requests.get(url, headers = headers)
    
    if response.status_code == 200:
        commits = response.json()
        len_commit = len(commits)
        if len_commit > 0:
            last_commit = commits[0]['commit']['committer']['date'][:10]
            return {
                "length": len_commit,
                "last_commit": last_commit
            }
        else:
            return None  # No commits in the repository
    elif response.status_code == 404:
        return "404"
    elif response.status_code == 409:
        return "409"
    elif response.status_code == 401:
        return "401"
    elif response.status_code == 451:
        return "451"
    
    elif response.status_code == 403 and "rate limit" in response.text.lower():
        raise RateLimitException("Rate limit exceeded. Retrying...")
    else:
        response.raise_for_status()  # Raise an exception for other status codes

class RateLimitException(Exception):
    pass       

try:
    # file_commit2023 = open("Logs/repo_commited_in_2023.txt", "w")
    # file_commit2023_errors = open("Logs/repo_commited_in_2023_errors.txt", "w")
    commit_collection_100000 = open("Logs/repo_100000.txt", "a")
    commit_collection_100000_errors = open("Logs/repo_100000_errors.txt", "a")
    for item in repo_values:
        repoinfo = item[2]

        commit_status = get_commit_status(repoinfo)

        if isinstance(commit_status, dict):
            print(commit_status)
            text = f'{item[0]},{repoinfo},{item[3]},{str(commit_status["length"])},{commit_status["last_commit"]}\n'
            print(text)
            commit_collection_100000.writelines(text)
        
        elif commit_status == "401":
            print(item[0], "401")
            text = f'{item[0]},{repoinfo}, 401\n'
            commit_collection_100000_errors.writelines(text)

        elif commit_status == "404":
            print(item[0], "404")
            text = f'{item[0]},{repoinfo}, 404\n'
            commit_collection_100000_errors.writelines(text)

        elif commit_status == "409":
            text = f'{item[0]},{repoinfo}, 409 empty\n'
            commit_collection_100000_errors.writelines(text)
            print(item[0], "409 empty")

        elif commit_status == "451":
            text = f'{item[0]},{repoinfo}, 451 Repository access blocked\n'
            commit_collection_100000_errors.writelines(text)
            print(item[0], "451 access blocked")
            

        else:
            text = f'{item[0]},{repoinfo}, not in 2023\n'
            # commit_collection_100000_errors.writelines(text)
            print("not in 2023")

except RateLimitException:
    print("Rate limit exceeded. Please try again later.")

