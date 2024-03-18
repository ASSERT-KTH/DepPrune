import sys
import os

def get_belonging_deps(dependencies, files):
    # collected_files = []
    belonging_deps = []
    for file in files:
        for dep in dependencies:
            split_str = dep + "/"
            split_parts = file.split(split_str)
            if len(split_parts) > 1 and all("node_modules" not in part for part in split_parts):
                # collected_files.append(file)
                if dep not in belonging_deps:
                    belonging_deps.append(dep)
                break
    return {
        "deps": belonging_deps
    }


if __name__ == "__main__":
    project = sys.argv[1]

    # bloated
    bloated_file_path = os.path.abspath(f'./stubbifier/Playground/{project}_stubbifier_bloated_candidates.txt')
    with open(bloated_file_path) as f:
        bloated_files = f.read().splitlines()
    
    # accessed
    accessed_file_path = os.path.abspath(f'./stubbifier/Playground/{project}_stubbifier_accessed_files.txt')
    with open(accessed_file_path) as f:
        accessed_files = f.read().splitlines()

    dep_path = os.path.abspath(f'./Playground/{project}/runtime_deps.txt')
    with open(dep_path) as f:
        deps = f.read().splitlines()

    bloated_result = get_belonging_deps(deps, bloated_files)
    bloated_deps = bloated_result["deps"]

    accessed_result = get_belonging_deps(deps, accessed_files)
    accessed_deps = accessed_result["deps"]

    output_dep_path = f'./Playground/{project}/stubbifier_accessed_deps.txt'
    output_dep_file = open(output_dep_path, "a")
    
    for item in accessed_deps:
        output_dep_file.writelines(item + '\n')

    output_udep_path = f'./Playground/{project}/unreachable_deps_stubbifier.txt'
    output_udep_file = open(output_udep_path, "a")
    unreachable = list(set(bloated_deps) - set(accessed_deps))
    print("unreachable deps", unreachable)
    for item in unreachable:
        # print(item)
        output_udep_file.writelines(item + '\n')