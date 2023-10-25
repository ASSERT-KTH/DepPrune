import sys
import os
project = sys.argv[1]
filename = sys.argv[2]

file_path = f'Playground/{project}/{filename}'
output_path = f'temp_log.txt'

line_length = 0
output_file = open(output_path, 'a')
if os.path.exists(file_path):
    with open(file_path, "r") as file:
        for line in file:
            # output_file.writelines(f"{project},{line}")
            if line.strip():  # Remove leading/trailing whitespace
                line_length += 1
# if os.path.getsize(file_path) != 0:
#     with open(file_path, "r") as file:
#         for line in file:
#             if line.strip():  # Remove leading/trailing whitespace
#                 line_length += 1
else:
    print(project + " no such file ==============================")

output_file = open(output_path, 'a')    
output_file.writelines(f"{project},{line_length}\n")