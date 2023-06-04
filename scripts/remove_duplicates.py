import sys

filename = sys.argv[1]

def remove_duplicate_lines(input_file):
    lines_seen = set()  # Set to store unique lines
    unique_lines = []

    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespaces
            if line not in lines_seen:
                lines_seen.add(line)
                unique_lines.append(line)

    with open(input_file, 'w') as file:
        for line in unique_lines:
            file.write(line + '\n')

# Example usage

remove_duplicate_lines(filename)
