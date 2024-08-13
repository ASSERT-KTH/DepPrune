import sys
import os
import json

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
def extract_direct_deps(pkg_json_path):
    try:
        with open(pkg_json_path, 'r') as file:
            package_data = json.load(file)
        
        dependencies = package_data.get('dependencies', {})
        dependency_names = list(dependencies.keys())
        return dependency_names
        
    except FileNotFoundError:
        print(f"File not found: {pkg_json_path}")
        return []

if __name__ == "__main__":
    project = sys.argv[1]
    folder = sys.argv[2]
    file_path = os.path.abspath(f'./{folder}/{project}/npm_test_opened_files.txt')
    dep_path = os.path.abspath(f'./{folder}/{project}/runtime_deps.txt')
    deps = get_run_deps(dep_path)

    with open(file_path) as f:
        opened_files = f.read().splitlines()
    print("deps", len(deps))

    result = collect_files(deps, opened_files)

    pkg_json_path = f'./{folder}/{project}/package.json'

    output_path = f'./{folder}/{project}/opened_runtime_files.txt'
    output_file = open(output_path, "a")
    for item in result["reachable_files"]:
        # print(item)
        output_file.writelines(item + '\n')

    output_dep_path = f'./{folder}/{project}/opened_runtime_deps.txt'
    output_dep_file = open(output_dep_path, "a")
    reachable = result["reachable_deps"]
    for item in reachable:
        # print(item)
        output_dep_file.writelines(item + '\n')
    
    unreachable = list(set(deps) - set(reachable))
    print("unreachable deps", unreachable)

    output_all_path = f'./{folder}/{project}/unreachable_os_all.txt'
    output_all_file = open(output_all_path, "a")
    for item in unreachable:
        # print(item)
        output_all_file.writelines(item + '\n')

    output_direct_path = f'./{folder}/{project}/unreachable_os_direct.txt'
    output_direct_file = open(output_direct_path, "a")
    output_indirect_path = f'./{folder}/{project}/unreachable_os_indirect.txt'
    output_indirect_file = open(output_indirect_path, "a")
    
    
    # seperate the deps by direct and indirect
    direct_names = extract_direct_deps(pkg_json_path)
    for dep_name in direct_names:
        direct_folder = 'node_modules/' + dep_name
        if direct_folder in unreachable:
            print("unreachable direct: ", dep_name)
            output_direct_file.writelines(direct_folder + '\n')
            unreachable.remove(direct_folder)
    
    for item in unreachable:
        output_indirect_file.writelines(item + '\n')
            

