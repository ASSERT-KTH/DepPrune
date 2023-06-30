import os
import re
import requests
import subprocess
import json

filePath = f'./Logs/target_103_loc_loc.txt'
with open(filePath) as f:
    lines = f.read().splitlines()

headers = {
    "Authorization": "Bearer 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"
}

# Regular expression pattern to match comment lines
comment_pattern = r"^\s*//.*|^\s*/\*.*?\*/|^\s*\*.*"

# Traverse the directory and count lines of code
def calc_loc(directory):
    lines_of_code = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith((".js", ".ts")):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    try:
                        for line in f:
                            # Exclude comment lines
                            if not re.match(comment_pattern, line):
                                lines_of_code += 1
                    except:
                        print("UnicodeDecodeError: invalid start byte")

    return lines_of_code


def get_commit_status(repoinfo):
    url = f"https://api.github.com/repos/{repoinfo}/commits"
    response = requests.get(url, headers = headers)
    
    if response.status_code == 200:
        commits = response.json()
        len_commit = len(commits)
        if len_commit > 0:
            latest_commit_sha = commits[0]['sha']
            last_commit = commits[0]['commit']['committer']['date'][:10]
            return {
                "latest_commit_sha": latest_commit_sha,
                "last_commit": last_commit
            }

def get_direct_deps(json_path):
    f_package = open(json_path, encoding="utf-8")  
    packageDict = json.load(f_package)
    if "dependencies" in packageDict.keys():
        directDeps = list(packageDict['dependencies'])
        print('directDeps: ', directDeps)
        return len(directDeps)
        # return directDeps
    return 0
    # return []

  



targetfile = open("Logs/target_103_loc_loc_loc.txt", "a")
for line in lines:
    item = line.split(',')
    folder = item[0]
    repoinfo = item[1]
    
    # Specify the directory containing your JavaScript and TypeScript files
    # directory = f"Original/{folder}"
    directory_node_modules = f"Original/{folder}/node_modules"

    # get git commit information
    # commit_status = get_commit_status(repoinfo)

    # calculate lines of code in the package
    # pac_loc = calc_loc(directory)
    # print("Total lines of code in packages:", pac_loc)

    
    # os.chdir("../..")
    # calculate lines of code in the dependencies
    dep_loc = 0 
    dep_loc = calc_loc(directory_node_modules)
    print("Total lines of code in dependencies:", dep_loc)

    # # calculate number of direct dependencies
    # package_json_path = f"Original/{folder}/package.json"
    # len_direct = get_direct_deps(package_json_path)
    # print("Number of direct dependencies:", len_direct)


    text = f'{line},{dep_loc}\n'
    targetfile.writelines(text)
