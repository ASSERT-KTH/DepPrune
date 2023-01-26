import sys
import json
import random

# randomly select from 918 projects with tests
projectsPath = f'top_491_with_deps_5_90.txt'
with open(projectsPath) as f:
    packages = f.read().splitlines()
    
randomNum = 100
randomPacks = random.sample(packages, randomNum)

random2Path = f'top_491_with_deps_5_90_random.txt'
random2File = open(random2Path, 'a')
for package in randomPacks:
    random2File.writelines(package + '\n')
random2File.close()
