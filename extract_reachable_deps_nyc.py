import sys

def get_run_deps(dep_path):
    runtime_deps = []

    with open(dep_path) as f:
        deps_original = f.read().splitlines()

    for dep in deps_original:
        runtime_deps.append(dep.split("__")[0])
    return runtime_deps

def collect_files(dependencies, files):
    collected_files = []
    reachable_deps = []
    for file in files:
        for dep in dependencies:
            split_str = dep + "/"
            split_parts = file.split(split_str)
            if len(split_parts) > 1 and all("node_modules" not in part for part in split_parts):
                collected_files.append(file)
                if dep not in reachable_deps:
                    reachable_deps.append(dep)
                break
    print("reachable_deps", len(reachable_deps))
    return {
        "reachable_files": collected_files,
        "reachable_deps": reachable_deps
    }

if __name__ == "__main__":
    project = sys.argv[1]

    reachable_file_path = f'Playground/{project}/reachable_files_nyc.txt'
    with open(reachable_file_path) as f:
        reachable_files = f.read().splitlines()

    dep_path = f'./Playground/{project}/runtime_deps.txt'
    deps = get_run_deps(dep_path)

    result = collect_files(deps, reachable_files)

    output_path = f'./Playground/{project}/reachable_runtime_files_nyc.txt'
    output_file = open(output_path, "a")
    for item in result["reachable_files"]:
        # print(item)
        output_file.writelines(item + '\n')

    output_dep_path = f'./Playground/{project}/reachable_runtime_deps_nyc.txt'
    output_dep_file = open(output_dep_path, "a")
    reachable = result["reachable_deps"]
    for item in reachable:
        # print(item)
        output_dep_file.writelines(item + '\n')

    output_udep_path = f'./Playground/{project}/unreachable_runtime_deps_nyc.txt'
    output_udep_file = open(output_udep_path, "a")
    unreachable = list(set(deps) - set(reachable))
    for item in unreachable:
        # print(item)
        output_udep_file.writelines(item + '\n')