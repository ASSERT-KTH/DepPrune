jsonlist=$(jq -r '.projects' "repos_copy2_2.json")

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
    echo "I am package "$repoUrl" ....." >> /dev/stderr

    file="./Playground/"$projectName"/indirect_bloated_deps.txt"

    mapfile -t lines < "$file"

    for line in "${lines[@]}"; do
        echo "$line"
        array=(${line//__/ })
        depname=${array[0]}
        depversion=${array[1]}
        echo $depname
        # git clone repo to temp folder, remove one direct dependency, run test, log, remove repo
        cd TestCollection2_2
        git clone $repoUrl $projectName
        cd $projectName
        git checkout $commit
        cp "../../Playground/"$projectName"/package-lock.json" ./package-lock.json
        # exclude dep from the lock file
        python3 ../../scripts/remove_indirect_deps.py $projectName $line
        echo "I am running test after removing dep "$line" ....."
        echo "I am running test after removing dep "$line" ....." >> /dev/stderr
        command_output=$(npm run test)
        if [[ $command_output == *$testPassSignal* ]]; then
            echo $projectName","$line",1" >> ../../test_result_output2_2.txt
        else
            echo $projectName","$line",0" >> ../../test_result_output_error2_2.txt
        fi
        cd ..
        rm -rf $projectName
        cd ..
    done
done