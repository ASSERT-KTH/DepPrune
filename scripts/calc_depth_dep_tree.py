import json
import sys

folder = sys.argv[1]

output_path = f'./temp_log.txt'

def calculate_dependencies_depth(data, depth=0):
    if isinstance(data, dict):
        if "dependencies" in data:
            return max(depth, calculate_dependencies_depth(data["dependencies"], depth + 1))
        else:
            if len(data) == 0: 
                return depth
            return max(calculate_dependencies_depth(value, depth) for value in data.values())
    
    elif isinstance(data, list):
        return max(calculate_dependencies_depth(item, depth) for item in data)
    
    else:
        return depth

def main():
    json_file_path = f"./Playground/{folder}/dependency-tree-npm.json"  # Replace this with the path to your JSON file

    with open(json_file_path) as file:
        data = json.load(file)

    dependencies_depth = calculate_dependencies_depth(data)
    print("Depth of the 'dependencies' key:", dependencies_depth)
    output_file = open(output_path, 'a')    
    output_file.writelines(f"{folder},{dependencies_depth}\n")

if __name__ == "__main__":
    main()
