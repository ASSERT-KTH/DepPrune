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
    echo $folderPath 

    # rm -rf $folderPath
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
    # rm -rf "${folderPath}/non-isolated-deps.txt"
    
    
    # git clone $repoUrl $folderPath

    # cd $folderPath

    # git checkout $commit

    # cd ../..

    # ./resetProject.sh $folderPath

    # python3 genDepList.py $folderPath "npm install "

    # python3 genNycRc.py $folderPath "${folderPath}/dep_list.txt" 
    
    # cd $folderPath

    # echo "Start Generating test coverage report..."

    # nyc npm run test

    # cd ../..

    # echo "Start discovering bloated files..."

    # ./transform.sh $folderPath "dynamic" false

    # python3 scripts/extract_unreachable_deps.py $projectName 

    # python3 scripts/extract_intersection.py $projectName 
    # python3 scripts/extract_multiple_versions.py $projectName 

    # npm list --all --omit=dev --json > dependency-tree-npm.json
    # npm list --all --omit=dev > npm_list_output.txt
    # grep -v "deduped" npm_list_output.txt > original_npm_list_filtered.txt
    # rm -rf npm_list_output.txt
    # cd ../..

    # python3 scripts/calc_depth_dep_tree.py $projectName
    python3 scripts/extract_empty_files.py $projectName
    # python3 scripts/build_deps_versions.py $projectName
    # python3 scripts/build_direct_bloated.py $projectName
    # python3 scripts/calculate_code_size.py $projectName
    # python3 scripts/calculate_symbolic_size.py $projectName
    # python3 scripts/extract_indirect_bloated_deps.py $projectName
    # python3 scripts/extract_twosides_deps.py $projectName
    # node scripts/dep-tree.js $folderPath $entryFile
    # python3 scripts/remove-deps-from-clients.py $projectName
    
done
