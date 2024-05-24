jsonlist=$(jq -r '.projects' "repos.json")

for row in $(echo "${jsonlist}" | jq -r '.[] | @base64')
do
    _jq()
    {
        echo ${row} | base64 --decode | jq -r ${1}
    }
    repoUrl=$(_jq '.gitURL')
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
    
    cd ../..
    # extract the list of runtime dependencies
    python3 identify_runtime_from_lock.py $projectName "Playground"


    echo "Start running test..."
    cd $folderPath
    # run test and trace open/openat .js/.json files at the OS level
    strace -f -e trace=open,openat -o npm_test_trace.txt npm run $unitTest
    # grep
    grep -E "open\(|openat\(" npm_test_trace.txt | awk -F, '{print $2}' | grep "/${projectName}" | grep -E ".js\"$|.json\"$" | sort | uniq > "npm_test_opened_files.txt"

    cd ../..

    echo "Start discovering bloated files and dependencies..."

    python3 extract_bloated_candidates.py $projectName "Playground"

done
