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
    file_path = f'./Playground/{project}/npm_test_opened_files.txt'
    dep_path = f'./Playground/{project}/runtime_deps.txt'
    deps = get_run_deps(dep_path)

    with open(file_path) as f:
        opened_files = f.read().splitlines()
    print("deps", len(deps))

    result = collect_files(deps, opened_files)

    output_path = f'./Playground/{project}/opened_runtime_files.txt'
    output_file = open(output_path, "a")
    for item in result["reachable_files"]:
        # print(item)
        output_file.writelines(item + '\n')

    output_dep_path = f'./Playground/{project}/opened_runtime_deps.txt'
    output_dep_file = open(output_dep_path, "a")
    reachable = result["reachable_deps"]
    for item in reachable:
        # print(item)
        output_dep_file.writelines(item + '\n')

    output_udep_path = f'./Playground/{project}/unreachable_runtime_deps_os.txt'
    output_udep_file = open(output_udep_path, "a")
    unreachable = list(set(deps) - set(reachable))
    for item in unreachable:
        # print(item)
        output_udep_file.writelines(item + '\n')