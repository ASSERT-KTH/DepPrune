# import sys
# import os

# project = sys.argv[1]

filePath = "test_direct_result_output.txt"
with open(filePath) as f:
    lines = f.read().splitlines()

confirmed_dict = {}
for line in lines:
    arr = line.split(",")
    pck_name = arr[0]
    dep_name = arr[1]
    if pck_name not in confirmed_dict:
        confirmed_dict[pck_name] = []
    confirmed_dict[pck_name].append(dep_name)

for key, value in confirmed_dict.items():
    print(key)
    output_file = open(f'./Playground/{key}/direct-confirmed-deps.txt', "a")
    for item in value:
        output_file.writelines(item+"\n")
    