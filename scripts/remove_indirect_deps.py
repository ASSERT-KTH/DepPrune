import sys
import json
import os
import subprocess

project = sys.argv[1]
dep = sys.argv[2]

test_output_file = f'../../Playground/{project}/indirect_test_output.txt'

relative_path = f'../../Playground/{project}/non-isolated-clients.json'
filePath = os.path.abspath(relative_path)
f_package = open(filePath, encoding="utf-8")  
clientsDict = json.load(f_package)
print(clientsDict)

old_path_pre = f"/data/js-variants/multee/Playground/{project}/" 
new_path_pre = f"/data/js-variants/multee/TestCollection/{project}/"


depInfo = dep.split("__")
depName = depInfo[0]
depVersion = depInfo[1]

# exclude the dep from package-lock.json
result = subprocess.run(["python3", os.path.abspath("../../scripts/exclude_indirect_dep.py"), depName, depVersion, project], stdout=subprocess.PIPE, text=True)
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


# print("I am running test!!! for " + dep)
# test_passed = "1"
# test_result = subprocess.run(["npm", "test"], capture_output=True, text=True, shell=True)
# if test_result.returncode == 0:
#     print("test result output:")
#     print(test_result.stdout)
#     if test_result.stdout != "None":
#         test_passed = "0"

# else:
#     test_passed = "0"
#     print("JavaScript script returned a non-zero exit code.")

# newFile = open(test_output_file, 'a')
# newFile.writelines(project + "," + dep + "," + test_passed + '\n')
