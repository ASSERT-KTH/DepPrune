jsonlist=$(jq -r '.projects' "repos_92.json")

# inside the loop, you cant use the fuction _jq() to get values from each object.
for row in $(echo "${jsonlist}" | jq -r '.[] | @base64')
do
    _jq()
    {
        echo ${row} | base64 --decode | jq -r ${1}
    }
    repoUrl=$(_jq '.gitURL')
    entryFile=$(_jq '.entryFile')
    projectName=$(_jq '.folder')
    folderPath="Playground/"$(_jq '.folder')
    commit=$(_jq '.commit')

    # echo $repoUrl 
    # echo $folderPath 

    # rm -rf $folderPath
    # rm -rf "${folderPath}/npm_list_output.txt"
    # rm -rf "${folderPath}/dep_list.txt"
    # rm -rf "${folderPath}/dependency-tree-list.txt"
    # rm -rf "${folderPath}/dependency-tree-npm.json"
    # rm -rf "${folderPath}/dependency-tree.json"
    # rm -rf "${folderPath}/direct-deps.txt"
    # rm -rf "${folderPath}/potential-deps.txt"
    # rm -rf "${folderPath}/reachable-deps.txt"
    # rm -rf "${folderPath}/total-files.txt"
    # rm -rf "${folderPath}/unused-deps.txt"
    # rm -rf "${folderPath}/unused-files.txt"
    # rm -rf "${folderPath}/used-files.txt"
    # rm -rf "${folderPath}/value_map.json"
    # rm -rf "${folderPath}/direct_bloated_deps.txt"
    # rm -rf "${folderPath}/original_npm_list_filtered.txt"
    # rm -rf "${folderPath}/dep_versions.json"
    # rm -rf "${folderPath}/dependent-files.json"
    # rm -rf "${folderPath}/isolated-deps.txt"
    # rm -rf "${folderPath}/non-isolated-clients.json"
    # rm -rf "${folderPath}/dependent-files-total.json"
    # rm -rf "${folderPath}/non-isolated-deps.txt"
    # rm -rf "${folderPath}/total_deps.txt"
    # rm -rf "${folderPath}/direct-confirmed-deps.txt"
    # rm -rf "${folderPath}/indirect-isolated-deps.txt"
    # rm -rf "${folderPath}/indirect_nonisolated_deps.txt"
    # rm -rf "${folderPath}/reachable_confirmed_deps.txt"

    # python3 scripts/calc_depth_dep_tree.py $projectName
    python3 scripts/extract_empty_files.py $projectName
    # python3 scripts/build_direct_bloated.py $projectName
    # python3 scripts/calculate_code_size.py $projectName
    # python3 scripts/calculate_symbolic_size.py $projectName
    # python3 scripts/extract_indirect_bloated_deps.py $projectName
    # python3 scripts/extract_twosides_deps.py $projectName
    # node scripts/dep-tree.js $folderPath $entryFile
    # python3 scripts/remove-deps-from-clients.py $projectName
    # python3 scripts/extract_depinfo_from_npm.py $projectName
    # python3 scripts/extract_duplicates.py $projectName
    # python3 scripts/extract_difference.py $projectName
    # python3 scripts/extract_intersection.py $projectName
    # python3 scripts/extract_isolated_deps_from_total.py $projectName
    # python3 scripts/extract_twosides_deps.py $projectName
    # python3 scripts/extract_dep_location.py $projectName
    # python3 scripts/remove_duplicates.py "${folderPath}/non-bloated_deps_location.txt"
    # node scripts/dep-tree-total.js $folderPath $entryFile
    # node scripts/dep-tree-list.js $folderPath $entryFile 
    

    # cd $folderPath
    
    # original=$(($(wc -l < original_npm_list_filtered.txt) - 2))
    # npm list --all --omit=dev > npm_list_output.txt
    # extraction=$(wc -l < total_deps.txt)
    # unmet=$(grep -c "UNMET" original_npm_list_filtered.txt)
    # difference=$(( $(($original - $unmet)) - $extraction))
    # echo $difference
    # cd ../..
done