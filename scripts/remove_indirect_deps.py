import sys
import json
import os
import subprocess

project = sys.argv[1]
dep = sys.argv[2]

if __name__ == "__main__":
    relative_path = f'../../Playground/{project}/non-isolated-clients.json'
    filePath = os.path.abspath(relative_path)
    f_package = open(filePath, encoding="utf-8")  
    clientsDict = json.load(f_package)

    old_path_pre = f"/data/js-variants/multee/Playground/{project}/" 
    new_path_pre = f"/data/js-variants/multee/TestCollection/{project}/"


    depInfo = dep.split("__")
    depName = depInfo[0]
    depVersion = depInfo[1]

    # exclude the dep from package-lock.json
    result = subprocess.run(["python3", os.path.abspath("../../scripts/"), depName, depVersion, project], stdout=subprocess.PIPE, text=True)
    # build the package with a modified lock file
    subprocess.run(["npm", "install"], check=True)


    # remove statements from the client files after building(installation)
    if dep in clientsDict:
        targetFiles = clientsDict.get(dep)

        for item in targetFiles:
            targetFile = item.replace(old_path_pre, new_path_pre)
            if os.path.exists(targetFile):
                result1 = subprocess.run(["node", os.path.abspath("../../scripts/remove_deps_originally.js"), targetFile, depName])
                if result1.returncode == 0:
                    print("remove_deps output:")
                    print(result1.stdout)

                else:
                    print("JavaScript script returned a non-zero exit code.")
