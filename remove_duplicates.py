import sys

filename = sys.argv[1]

def remove_duplicate_lines(input_file):
    lines_seen = set()  # Set to store unique lines
    unique_lines = []
    print("input_file", input_file)

    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespaces
            if line not in lines_seen:
                lines_seen.add(line)
                unique_lines.append(line)
    output_file = str(input_file)[:-4] + "_deduped.txt"
    print(output_file)
    with open(output_file, 'w') as file:
        for line in unique_lines:
            file.write(line + '\n')

# Example usage
remove_duplicate_lines(filename)