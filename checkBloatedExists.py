import sys
import os

project = sys.argv[1]

file_path = f'./Playground/{project}/unreachable_runtime_deps_removed.txt'
with open(file_path) as f:
    lines = f.read().splitlines()

for line in lines:
    folder = f'./TestWithDebloatedLock/{project}/{line}'
    if os.path.exists(folder):
        print(line, " has been installed")
    else:
        print(666)