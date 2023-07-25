
input_file = f"deps_info_log.txt"
with open(input_file) as f:
    deps = f.read().splitlines()
output_file = f"deps_info_with_size.txt"

def extract_string_from_line(line, start_substring, end_substring):
    start_index = line.find(start_substring)
    if start_index != -1:
        start_index += len(start_substring)
        end_index = line.find(end_substring, start_index)
        if end_index != -1:
            return line[start_index:end_index]

    return None

def extract_specific_string(file_path, start_substring, end_substring):
    with open(file_path, "r") as file:
        for line in file:
            extracted_string = extract_string_from_line(line, start_substring, end_substring)
            if extracted_string is not None:
                return extracted_string

    return None

if __name__ == "__main__":
    file_path = "deps_info_size_log.txt"
    end_substring = " KB"
    output_f = open(output_file, 'a')
    for dep in deps:
        start_substring = dep
        extracted_string = extract_specific_string(file_path, start_substring, end_substring)
        item = f"{dep},{extracted_string}\n"
        output_f.write(item)  
        print(item)
