import json
import os
import sys

def read_json_file(file_path):
    """Read a JSON file and return its content."""
    with open(file_path, 'r') as file:
        return json.load(file)

def read_txt_file(file_path):
    """Read a text file and return its content as a set of lines."""
    with open(file_path, 'r') as file:
        return set(line.strip() for line in file)

def write_to_file(file_path, lines):
    """Write lines to a file."""
    with open(file_path, 'w') as file:
        for line in lines:
            file.write(f"{line}\n")

def main(project_name):
    # Define the paths to the input and output files based on the project name
    package_json_path = f'Playground/{project_name}/package.json'
    txt_file_path = f'Playground/{project_name}/unreachable_runtime_deps_os.txt'
    output_file_path = f'Playground/{project_name}/direct_bloated_deps.txt'
    
    # Check if the package.json file exists
    if not os.path.exists(package_json_path):
        print(f"Error: {package_json_path} does not exist.")
        return
    
    # Check if the txt file exists
    if not os.path.exists(txt_file_path):
        print(f"Error: {txt_file_path} does not exist.")
        return

    # Read the package.json file
    package_data = read_json_file(package_json_path)
    
    # Get the dependencies from package.json
    dependencies = package_data.get("dependencies", {}).keys()

    # Read the txt file and get the available paths
    available_paths = read_txt_file(txt_file_path)
    
    # Find matching paths
    matching_paths = set()
    for dep in dependencies:
        dep_path = f"node_modules/{dep}"
        if dep_path in available_paths:
            matching_paths.add(dep_path)
    
    # Write the matching paths to the output file
    write_to_file(output_file_path, matching_paths)
    print(f"Output written to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <project_name>")
        sys.exit(1)
    
    # Get the project name from the command-line argument
    project_name = sys.argv[1]
    
    # Run the main function with the provided project name
    main(project_name)

