# For a specific package, 
# if there is no direct bloated deps, 
# then all the potential-deps are indirect dependencies.
# Else, take away direct_bloated_deps from potential-deps, add both direct_indirect_bloated_deps.
# store the result in indirect_bloated_deps.txt

import sys
import os

project = sys.argv[1]
indirect_bloated = []

potential_path = f'Playground/{project}/potential-deps.txt'
with open(potential_path) as f:
    potential_deps = f.read().splitlines()

direct_path = f'Playground/{project}/direct_bloated_deps.txt'
if not os.path.exists(direct_path):
    indirect_bloated = potential_deps
if os.path.getsize(direct_path) == 0:
    indirect_bloated = potential_deps
else:
    with open(direct_path) as f:
        direct_deps = f.read().splitlines()
        indirect_bloated = list(set(potential_deps).difference(set(direct_deps)))
        both_path = f'Playground/{project}/direct_indirect_bloated_deps.txt'
        if os.path.getsize(both_path) != 0:
            with open(both_path) as f:
                both_deps = f.read().splitlines()
            indirect_bloated = indirect_bloated + both_deps

print(len(indirect_bloated))

indirect_path = f'Playground/{project}/indirect_bloated_deps.txt'
indirect_deps_file = open(indirect_path, "a")
for item in indirect_bloated:
    indirect_deps_file.writelines(item + '\n')
