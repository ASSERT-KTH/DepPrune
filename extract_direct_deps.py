
import sys
import os
from utils import get_direct_deps, get_dep_version

project = sys.argv[1]

direct_path = f'Playground/{project}/direct_deps.txt'
json_path = f'Playground/{project}/package.json'
direct_deps = get_direct_deps(json_path)
direct_file = open(direct_path, "a")
for item in direct_deps:
    name = item
    version = get_dep_version(item, project)
    dep = name + "__" + version
    direct_file.writelines(dep + '\n')