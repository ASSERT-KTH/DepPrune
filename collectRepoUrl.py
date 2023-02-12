import sys
import json
import os

# import random

# project = sys.argv[1]
# filePath = f'./Data/{project}/{project}_dependants_url.txt'
# newFilePath = f'./Data/{project}/{project}_dependants_url_100.txt'

# # deduplicate
# filePath = f'developmentCollected_250.txt'
# newFilePath = f'developmentCollected_deduplicated.txt'
# # filePath = f'productions_in_3000.txt'
# # newFilePath = f'productions_in_3000_deduplicated.txt'

# with open(filePath) as f:
#     lines = f.read().splitlines()

# lines = list(dict.fromkeys(lines))

# newFile = open(newFilePath, 'w')
# for line in lines:
#     newFile.writelines(line + '\n')
# newFile.close()



# remove duplicated repo link
# filePath = f'top3000_url.txt'
# newFilePath = f'top3000_url_deduplicated.txt'
# duplicatedFilePath = f'top3000_url_duplicated.txt'
# urlList = []
# duplicatedList = []

# with open(filePath) as f:
#     lines = f.read().splitlines()

# newFile = open(newFilePath, 'w')
# duplicatedFile = open(duplicatedFilePath, 'a')

# for line in lines:
#     row = line.split(',')
#     url = row[1]
#     if url == 'null' or url == 'undefined' or url == 'https://github.com/null':
#         continue 
#     if url in urlList:
#         duplicatedFile.writelines(line + '\n')
#     if url not in urlList:
#         urlList.append(url)
#         newFile.writelines(line + '\n')

# newFile.close()
# duplicatedFile.close()


# # replace package name with repo folder name 
# filePath = f'top3000_url_deduplicated.txt'
# newFilePath = f'top3000_folder.txt'

# with open(filePath) as f:
#     lines = f.read().splitlines()

# newFile = open(newFilePath, 'w')

# for line in lines:
#     row = line.split(',')
#     project = row[0]
#     url = row[1]
#     urlArr = url.rsplit('/', 1)
#     folderName = urlArr[1]

#     newFile.writelines(folderName + ',' + url + '\n')

# newFile.close()

# # # calculate direct dependencies, transitive dependencies
# totalDeps = []
# extraneousDeps = []
# directDepsLen = 0
# # scan production dependencies from npm list
# def get_production_deps(dictionary):
#     for key, value in dictionary.items():
#         if key == "dependencies" and isinstance(value, dict):
#             childDict = value
#             output = list(childDict.keys())
#             for subKey, subValue in childDict.items():
#                 for subSubKey, subSubValue in subValue.items():
#                     if subSubKey == "extraneous" and subSubValue == True:
#                         extraneousDeps.append(subSubKey)
#             for dep in output:
#                 totalDeps.append(dep)
#             for itemKey, itemValue in childDict.items():
#                 get_production_deps(itemValue)

# def get_direct_deps(dictionary):
#     if "dependencies" in dictionary.keys():
#         directDeps = list(dictionary['dependencies'])
#         # print('directDeps: ', directDeps)
#         return len(directDeps)
#     return 0

# def has_test(dictionary):
#     if "scripts" in dictionary.keys():
#         scripts = list(dictionary['scripts'])
#         if "test" in scripts:
#             return True
#     return False


# filePath_package = f'package.json'    
# f_package = open(filePath_package, encoding="utf-8")  
# packageDict = json.load(f_package)
# directDepsLen = get_direct_deps(packageDict)


# filePath_deps = f'productionDependenciesNew.json'
# f_deps = open(filePath_deps, encoding="utf-8")
# productionDict = json.load(f_deps)
# get_production_deps(productionDict)

# extraneousDepsLen = len(extraneousDeps)
# totalDepsLen = len(totalDeps) - extraneousDepsLen
# transDepsLen = totalDepsLen - directDepsLen

# if (totalDepsLen >= 5 and totalDepsLen <= 92):
#     line = project + ',' + str(extraneousDepsLen) + "," + str(directDepsLen) + "," + str(transDepsLen) + ',' + str(totalDepsLen) + '\n'
# # line = str(totalDepsLen) + ','
#     productionDepPath = f'../../top_dependencies_5_92.txt'
#     productionsFile = open(productionDepPath, 'a')

#     productionsFile.writelines(line)
#     productionsFile.close()


# # collect productions from the dataset of the production packages
# originalPath = f'top3000_url_deduplicated.txt'
# productionsFilePath = f'productionCollected_deduplicated.txt'
# productionsInTopPath = f'productions_in_3000.txt'
# productions = []

# with open(productionsFilePath) as f:
#     productions = f.read().splitlines()

# with open(originalPath) as f:
#     originals = f.read().splitlines()

# newFile = open(productionsInTopPath, 'a')
# for item in originals:
#     row = item.split(',')
#     project = row[0]
#     if project in productions:
#         newFile.writelines(item + '\n')
# newFile.close()



# # scan development dependencies from npm list
# def get_development_deps(dictionary, depsFile):

#     for key, value in dictionary.items():

#         if key == "dependencies" and isinstance(value, dict):
#             childDict = value
#             output = list(childDict.keys())
#             print(output)
#             for dep in output:
#                 # depStr = "" + dep
#                 print(dep)
#                 depsFile.writelines(dep + '\n')
            
#             # for itemKey, itemValue in childDict.items():
#             #     get_development_deps(itemValue, depsFile)

# project = sys.argv[1]

# filePath = f'./Original/{project}/developmentDependencies.json'
# developmentDepPath = f'developmentCollected_250.txt'
# developmentsFile = open(developmentDepPath, 'a')
# f = open(filePath, encoding="utf-8")
# developmentDict = json.load(f)
# # print(developmentDict)
# devDependencies = get_development_deps(developmentDict, developmentsFile)
# developmentsFile.close()


# originalPath = f'top3000_url_deduplicated_onlyname.txt' # 1361
# developmentPath = f'developmentCollected_deduplicated.txt' # 1655
# productionsFilePath = f'productions_in_3000_onlyname.txt' # 210
# productionsInTotalFilePath = f'productionCollected_deduplicated.txt' # 1999

# developmentsInTopPath = f'developments_in_3000.txt'
# productions = []

# with open(productionsFilePath) as f:
#     productions = f.read().splitlines() # 210
# print(len(productions))

# with open(productionsInTotalFilePath) as f:
#     productionsInTotal = f.read().splitlines() # 1999
# print(len(productionsInTotal))

# with open(developmentPath) as f:
#     developments_withPro = f.read().splitlines() # 1655
# print(len(developments_withPro))

# with open(originalPath) as f: # 1361
#     originals = f.read().splitlines()
# print(len(originals))

# intersection_direct = list(set(developments).intersection(set(productionsInTotal)))
# print(len(intersection_direct))

# intersection_direct_in1361 = list(set(intersection_direct).intersection(set(originals)))
# print(len(intersection_direct_in1361))

# intersection_production_original = list(set(productions).intersection(set(originals)))
# print(len(intersection_production_original))

# difference = list(set(developments).difference(set(productions)))
# print(len(difference))

# newFile = open(developmentsInTopPath, 'a')
# for item in originals:
#     print(item)
#     row = item.split(',')
#     projectName = row[0]
#     print(projectName)
#     if projectName in developments and projectName not in productions:
#         newFile.writelines(item + '\n')
# newFile.close()

# # make up packages
# OriginalPath = f'top_491_with_deps_5_90.txt'
# newPath = f'top_dependencies_5_92.txt'
# resultPath = f'top_in_original_outof_new.txt'
# result2Path = f'top_in_new_outof_original.txt'

# with open(OriginalPath) as f:
#     originals = f.read().splitlines()

# with open(newPath) as f:
#     news = f.read().splitlines()

# shouldRemove = list(set(originals).difference(set(news)))
# shouldAdd = list(set(news).difference(set(originals)))

# resultFile = open(resultPath, 'a')
# for item in shouldRemove:
#     resultFile.writelines(item + '\n')
# resultFile.close()

# result2File = open(result2Path, 'a')
# for item in shouldAdd:
#     result2File.writelines(item + '\n')
# result2File.close()

# # pick up package name
# filePath = f'top3000_url_deduplicated.txt'
# resultPath = f'top3000_url_deduplicated_onlyname.txt'

# with open(filePath) as f:
#     packages = f.read().splitlines()

# resultFile = open(resultPath, 'a')
# for item in packages:
#     row = item.split(',')
#     project = row[0]
#     resultFile.writelines(project + '\n')
# resultFile.close()


# randomly select from 918 projects with tests
# projectsPath = f'top_dependencies_greater1_test.txt'
# with open(projectsPath) as f:
#     packages = f.read().splitlines()
    
# randomNum = 30
# randomPacks = random.sample(packages, randomNum)

# random2Path = f'top_dependencies_greater1_test_random.txt'
# random2File = open(random2Path, 'a')
# for package in randomPacks:
#     random2File.writelines(package + '\n')
# random2File.close()

# random.sample(list, n)

# # # get repo links and number of dependencies
# filePath1 = f'top_coverage_80_100.txt'
# filePath2 = f'top1448_unique_commit.txt'
# filePath3 = f'top_dependencies_greater1.txt'
# resultPath = f'top_coverage_80_100_info.txt'

# with open(filePath1) as f:
#     packages = f.read().splitlines()
# with open(filePath2) as f:
#     packageRepos = f.read().splitlines()
# with open(filePath3) as f:
#     packageDeps = f.read().splitlines()

# resultFile = open(resultPath, 'a')
# for item in packageRepos:
#     itemRepo = item.split(',')
#     project = itemRepo[0]
#     if project in packages:
#         print(project)
#         for itemDep in packageDeps:
#             print(itemDep)
#             dep = itemDep.split(',')
#             projectDep = dep[0]
#             if projectDep == project:
#                 projectStr = item + ',' + dep[1] + ',' + dep[2] + ',' + dep[3] + ',' + dep[4]
#                 resultFile.writelines(projectStr + '\n')
# resultFile.close()


# # transform txt to json
# filePath1 = f'top_coverage_80_100_info.txt'
# with open(filePath1) as f:
#     packages = f.read().splitlines()

# jsonArr = []

# for item in packages:
#     itemArr = item.split(',')
#     projectName = itemArr[0]
#     repoUrl = itemArr[1] + '.git'
#     commit = itemArr[2]
#     jsonDict = {
#         "gitURL": repoUrl,
#         "entryFile": "",
#         "folder": projectName,
#         "commit": commit
#     }
#     jsonArr.append(jsonDict)

# projectDict = {
#     "projects": jsonArr
# }

# with open('json.txt', 'w') as json_file:
#   json.dump(projectDict, json_file)


# curPath = os.getcwd()

# dirInData = os.listdir(curPath + '/Data')
# # dirInPlayground = os.listdir(curPath + '/Playground')
# print(dirInData)
# emptyDeps = []

# for item in dirInData:
#     funcPath = 'Data/' + item + '/' + item + '_bloated_functions.txt'
#     if not os.path.exists(funcPath):
#         print(item)
#         emptyDeps.append(item)

# for item in emptyDeps:
#     resultFile = open('top_target_untested_without_functions.txt', 'a')
#     resultFile.writelines(item + '\n')
#     resultFile.close()


# print(os.path.getsize())

with open('top_target_untested_empty.txt') as f:
    packages = f.read().splitlines()

with open('top_target_untested_without_functions.txt') as f:
    tested = f.read().splitlines()

difference = list(set(packages).difference(set(tested)))
print(difference)


