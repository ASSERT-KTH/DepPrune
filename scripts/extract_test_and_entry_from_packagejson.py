import requests

filePath = f'./Logs/repo_100000_branch_rest.txt'

with open(filePath) as f:
    lines = f.read().splitlines()

test_filePath = f'./Logs/repo_100000_test.txt'
error_filePath = f'./Logs/repo_100000_testentry_error.txt'
entry_filePath = f'./Logs/repo_100000_entry.txt'

test_file = open(test_filePath, 'a')
error_file = open(error_filePath, 'a')
entry_file = open(entry_filePath, 'a')


def fetch_pck(item):
    line = item.split(',')
    branch = line[5]
    repo = line[1]
    raw_file_url = f'https://raw.githubusercontent.com/{repo}/{branch}/package.json'

    # Make the HTTP GET request
    response = requests.get(raw_file_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Access the content of the response
        package_json_content = response.json()  # Assuming the file is in JSON format
        # Extract the "scripts" field from package.json
        scripts = package_json_content.get("scripts", {})
        print(repo)
        test_in = fetch_scripts(scripts, repo, branch)

        if test_in:
            entry = package_json_content.get("main", {})
            entry_return = fetch_entry(entry, repo, branch)
            if not entry_return is False:
                entry_file.writelines(repo + ',' + branch + ',' + entry_return + '\n')
            
    else:
        print(repo)
        print("Failed to retrieve the package.json file. Status code:", response.status_code)
        error_file.writelines(repo + ', no package.json \n')

def fetch_scripts(scripts, repo, branch):
    if len(scripts) == 0:
        error_file.writelines(repo + ', no script \n')
        return False

    if "test" not in scripts.keys():
        error_file.writelines(repo + ', no test \n')
        return False

    if "test" in scripts.keys():
        content = scripts['test']
        
        if "Error: no test specified" in content:
            error_file.writelines(repo + ',' + content + '\n')
            return False
        if "echo no-op" in content:
            error_file.writelines(repo + ',' + content + '\n')
            return False
        else:
            test_file.writelines(repo + ',' + branch + ',' + content + '\n')
            return True

    

def fetch_entry(mainfiled, repo, branch):
    if len(mainfiled) == 0:
        # If there is an index.js file in the root folder, return index.js
        entry_file_url = f'https://raw.githubusercontent.com/{repo}/{branch}/index.js'
        entryfile_response = requests.get(entry_file_url)
        if entryfile_response.status_code == 200:
            return "index.js"
        else:
            print("Failed to retrieve an entry file. Status code:", entryfile_response.status_code)
            error_file.writelines(repo + ", Failed to retrieve an entry file.\n")
            return False
    else:
        if mainfiled[-1] == '/':
            return mainfiled + 'index.js'
        if mainfiled[-3:] == '.js':
            return mainfiled
        else:
            error_file.writelines(repo + ", the entry file is not a js file.\n")
            return False
    



for item in lines:
    result = fetch_pck(item)
    

