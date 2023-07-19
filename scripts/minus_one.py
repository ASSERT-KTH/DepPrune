# import sys
# input_file = sys.argv[1]
# output_file = sys.argv[2]

# with open(input_file, "r") as input_f, open(output_file, "w") as output_f:
#     for line in input_f:
#         try:
#             number = int(line.strip())  
#             new_number = number - 1  
#             output_f.write(str(new_number) + "\n")  
#         except ValueError:
#             continue

# print("Done")
def extract_folder_name(file_path):
    parts = file_path.rsplit("/node_modules/", 1)
    if len(parts) == 2:
        folder_name = parts[1].split("/")[0]
        return folder_name
    else:
        return None

def get_dep_name(file_path):
    dep_name = file_path.split("/node_modules/")[1].split("/")[0]
    return dep_name

file_path = "/data/js-variants/multee/Playground/airtap/node_modules/JSONStream/test/bool.js"
result = extract_folder_name(file_path)

print(result)
