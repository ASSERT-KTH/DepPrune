jsonlist=$(jq -r '.projects' "repos_copy1.json")

# inside the loop, you cant use the fuction _jq() to get values from each object.
for row in $(echo "${jsonlist}" | jq -r '.[] | @base64')
do
    _jq()
    {
        echo ${row} | base64 --decode | jq -r ${1}
    }
    repoUrl=$(_jq '.gitURL')
    projectName=$(_jq '.folder')
    commit=$(_jq '.commit')
    testPassSignal=$(_jq '.testPassSignal')

    echo $repoUrl 
    
    echo "I am package "$repoUrl" ....."

    file="./Playground/"$projectName"/indirect_nonisolated_deps.txt"

    mapfile -t lines < "$file"
    if [ $lines -eq 0 ]; then
        echo "No deps. Exiting loop."
        break
    fi

    for line in "${lines[@]}"; do
        echo "$line"
        array=(${line//__/ })
        depname=${array[0]}
        depversion=${array[1]}
        echo $depname
        # git clone repo to temp folder, remove one direct dependency, run test, log, remove repo
        cd TestCollection
        git clone $repoUrl $projectName
        cd $projectName
        git checkout $commit
        cp "../../Playground/"$projectName"/package-lock.json" ./
        # exclude dep from the lock file
        python3 ../../scripts/exclude_indirect_dep.py $depname $depversion $projectName
        npm install
        # remove statements from client files
        python3 ../../scripts/remove_indirect_deps.py $projectName $line
        echo "I am running test after removing dep "$line" ....."
        command_output=$(npm run test 2>&1)
        if [[ $command_output == *$testPassSignal* ]]; then
            echo $projectName","$line",1" >> ../../test_indirect_result_output1.txt
        else
            echo $projectName","$line",0" >> ../../test_indirect_result_output_error1.txt
        fi
        cd ..
        rm -rf $projectName
        cd ..
    done
done