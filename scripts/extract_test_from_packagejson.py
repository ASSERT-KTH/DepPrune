import requests

filePath = f'./Logs/repo_commited_in_2023_branch.txt'
with open(filePath) as f:
    lines = f.read().splitlines()

testfilePath = f'./Logs/repo_commited_in_2023_test.txt'
test_error_filePath = f'./Logs/repo_commited_in_2023_test_error.txt'


def fetch_scripts(repo, branch):
    raw_file_url = f'https://raw.githubusercontent.com/{repo}/{branch}/package.json'

    # Make the HTTP GET request
    response = requests.get(raw_file_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Access the content of the response
        package_json_content = response.json()  # Assuming the file is in JSON format
        # Extract the "scripts" field from package.json
        scripts = package_json_content.get("scripts", {})
        if len(scripts) == 0:
            print(repo, "no script")
            return '0'

        if "test" in scripts.keys():
            print(repo)
            content = scripts['test']
            return content
        if "test" not in scripts.keys():
            return "notest"
            
    else:
        print("Failed to retrieve the package.json file. Status code:", response.status_code)
        return "nopackage"

testFile = open(testfilePath, 'a')
test_error_file = open(test_error_filePath, 'a')
for item in lines:
    line = item.split(',')
    branch = line[1]
    repoinfo = line[2]
    result = fetch_scripts(repoinfo, branch)
    if result == '0':
        test_error_file.writelines(repoinfo + ', no script \n')
    elif result == 'nopackage':
        test_error_file.writelines(repoinfo + ', no package.json \n')
    elif result == 'notest':
        test_error_file.writelines(repoinfo + ', no test \n')
    elif "Error: no test specified" in result:
        test_error_file.writelines(repoinfo + ',' + result + '\n')
    else:
        testFile.writelines(repoinfo + ', test:' + result + '\n')
    