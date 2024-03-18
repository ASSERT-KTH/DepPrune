import re
import sys

def extract_dependency_names(file_path, error_pattern):
    dependency_names = []
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(error_pattern, line)
            if match:
                dependency_name = match.group(1)
                if dependency_name not in dependency_names:
                    dependency_names.append(dependency_name)
    return dependency_names


def remove_deps_from_subset(file_path, deps):
    print(deps)
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            line_stripped = line.rstrip('\n')
            if not any(line_stripped.endswith(suffix) for suffix in deps):
                file.write(line)


if __name__ == "__main__":
    project = sys.argv[1]
    test_log_path = 'test_log.txt'
    file_path = f'Playground/{project}/true_bloated_in_stubbifier.txt'
    error_pattern = r"Error: Cannot find module '([^']+)'"
    dependency_names = extract_dependency_names(test_log_path, error_pattern)
    deps_to_remove = []
    if len(dependency_names) > 0:
        for dep in dependency_names:
            dep_folder = f'node_modules/{dep}'
            deps_to_remove.append(dep_folder)
        remove_deps_from_subset(file_path, deps_to_remove)
        print("True")
    else:
        print("False")
