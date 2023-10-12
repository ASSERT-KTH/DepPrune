file_path = f'all_bloated_deps.txt'
output_path = f'all_bloated_deps_count.txt'
deps_dict = {}
# {
#     "abbrev__1.1.1": 8
# }


with open(file_path, "r") as file:
    for line in file:
        item = line[:-1]
        if item not in deps_dict:
            deps_dict[item] = 1
        else:
            deps_dict[item] = deps_dict[item] + 1

output_file = open(output_path, 'a')    
for item in deps_dict:
    output_file.writelines(item + "," + str(deps_dict[item]) + "\n")