jsonlist=$(jq -r '.projects' "repos.json")

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
    
    git clone $repoUrl $folderPath

    cd $folderPath

    # git checkout $commit

    cp "../../LockFiles/${projectName}/package-lock.json" ./

    npm install
    # npm run test

    npm list --all --omit=dev > npm_list_output.txt
    grep -v "deduped" npm_list_output.txt > original_npm_list_filtered.txt
    cd ../..
    
    # generate the list of dependencies
    python3 ./extract_depinfo_from_npm.py $projectName "Playground"

    # generate .nycrc
    python3 generate_nycrc.py $folderPath "${folderPath}/total_deps_name.txt" 
    
    cd $folderPath

    echo "Start Generating test coverage report..."

    nyc npm run test

    cd ../..

    echo "Start discovering bloated files and dependencies..."
    python3 extract_reachable_files.py $projectName
    python3 extract_reachable_deps.py $projectName
    python3 extract_direct_deps.py $projectName 
    python3 remove_duplicates.py $folderPath"/total_deps.txt"
    python3 extract_difference.py $projectName "total_deps_deduped.txt" "reachable_deps.txt" "unreachable_deps.txt"
    python3 extract_intersection.py $projectName "unreachable_deps.txt" "direct_deps.txt" "direct_unreachable.txt"

    # npm list --all --omit=dev --json > dependency-tree-npm.json
    # npm list --all --omit=dev > npm_list_output.txt
    # grep -v "deduped" npm_list_output.txt > original_npm_list_filtered.txt
    # rm -rf npm_list_output.txt
    # cd ../..

    # python3 scripts/build_deps_versions.py $projectName
    # python3 scripts/build_direct_bloated.py $projectName
    
done
