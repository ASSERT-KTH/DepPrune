import os
import re
import requests
import subprocess

filePath = f'./Logs/repo_NodeJS_100000_copy.txt'
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
                    for line in f:
                        # Exclude comment lines
                        if not re.match(comment_pattern, line):
                            lines_of_code += 1
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

# Print the total lines of code


targetfile = open("Logs/repo_NodeJS_100000_loc.txt", "a")
targetfile_error = open("Logs/repo_NodeJS_100000_loc_error.txt", "a")
for line in lines:
    item = line.split(',')
    folder = item[0]
    repoinfo = item[1]
    
    git_url = f"https://github.com/{repoinfo}.git"

    # Specify the directory containing your JavaScript and TypeScript files
    directory = f"TestCollection/{folder}"
    directory_node_modules = f"TestCollection/{folder}/node_modules"

    commit_status = get_commit_status(repoinfo)
    print(commit_status["latest_commit_sha"])
    print(commit_status["last_commit"])

    # Git clone command
    git_clone_cmd = ["git", "clone", git_url, directory]

    # NPM install command
    npm_install_cmd = ["npm", "install"]

    # Execute Git clone
    subprocess.run(git_clone_cmd, check=True)

    # calculate lines of code in the package
    pac_loc = calc_loc(directory)
    print("Total lines of code in packages:", pac_loc)

    # Change directory to the cloned repository
    os.chdir(directory)
    print(os.getcwd())

    # Execute npm install
    # rm_lock = ["rm", "-rf", "package-lock.json"]
    # subprocess.run(rm_lock, check=True)

    try:
        result = subprocess.run(npm_install_cmd, check=True, capture_output=True, text=True)
        # Process the result as needed
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.returncode}\nOutput: {e.output}")
        error_text = f'{repoinfo}, Error: {e.returncode}, install error\n'
        targetfile_error.writelines(error_text)


    
    os.chdir("../..")
    # calculate lines of code in the dependencies
    dep_loc = 0 
    try:
        dep_loc = calc_loc(directory_node_modules)
        print("Total lines of code in dependencies:", dep_loc)
    except:
        error_text = f'{repoinfo}, count error\n'
        targetfile_error.writelines(error_text)

    rm_cmd = ["rm", "-rf", directory]
    print(os.getcwd())

    # Execute the rm -rf command
    subprocess.run(rm_cmd, check=True)

    text = f'{folder},{repoinfo},{pac_loc},{dep_loc},{item[2]},{item[3]},{commit_status["last_commit"]},{commit_status["latest_commit_sha"]},{item[5]},{item[7]},{item[8]}\n'
    targetfile.writelines(text)


