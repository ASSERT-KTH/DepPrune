jsonlist=$(jq -r '.projects' "repo.json")

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
    unitTest=$(_jq '.unitTest')

    # echo $repoUrl 
    echo $folderPath 
    
    git clone $repoUrl $folderPath

    cd $folderPath

    git checkout $commit

    # cp "../../LockFiles/${projectName}/package-lock.json" ./

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

    nyc npm run $unitTest

    cd ../..

    echo "Start discovering bloated files and dependencies..."
    python3 extract_reachable_files.py $projectName

done
