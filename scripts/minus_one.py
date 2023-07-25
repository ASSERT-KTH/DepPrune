import sys
input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "r") as input_f, open(output_file, "a") as output_f:
    for line in input_f:
        try:
            # number = int(line.strip())  
            # new_number = number - 1
            items = line.split(',')  
            output_f.write(items[1])  
        except ValueError:
            continue

print("Done")

