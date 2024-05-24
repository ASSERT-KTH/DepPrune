import re
import sys

def extract_dependency_names(file_path, error_pattern):
    dependency_names = []
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(error_pattern, line)
            match1 = re.search(error_pattern1, line)
            if match or match1:
                dependency_name = match.group(1)
                if dependency_name not in dependency_names:
                    dependency_names.append(dependency_name)
    return dependency_names


def remove_deps_from_subset(file_path, deps):
    # print(deps)
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            line_stripped = line.rstrip('\n')
            no_scoped = True
            if "@" in deps[0] and line_stripped.startswith(deps[0]):
                no_scoped = False
            if not any(line_stripped.endswith(suffix) for suffix in deps) and no_scoped:
                file.write(line)


if __name__ == "__main__":
    project = sys.argv[1]
    test_log_path = f'test_log.txt'
    file_path = f'Playground/{project}/stubbifier_misclassified.txt'
    error_pattern = r"Cannot find module '([^']+)'"
    error_pattern1 = r'"([^"]+)" is not found'
    dependency_names = extract_dependency_names(test_log_path, error_pattern, error_pattern1)
    
    deps_to_remove = []
    if len(dependency_names) > 0:
        for dep in dependency_names:
            if "/" in dep:
                dep = dep.split('/')[0]
            dep_folder = f'node_modules/{dep}'
            deps_to_remove.append(dep_folder)
        remove_deps_from_subset(file_path, deps_to_remove)
        print("True")
    else:
        print("False")
