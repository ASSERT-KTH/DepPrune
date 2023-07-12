import sys
input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "r") as input_f, open(output_file, "w") as output_f:
    for line in input_f:
        try:
            number = int(line.strip())  
            new_number = number - 1  
            output_f.write(str(new_number) + "\n")  
        except ValueError:
            continue

print("Done")
