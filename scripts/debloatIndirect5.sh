jsonlist=$(jq -r '.projects' "repos_copy5.json")

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

    file="./Playground/"$projectName"/isolated_passed_deps.txt"

    mapfile -t lines < "$file"
    if [ $lines -eq 0 ]; then
        echo "No deps. Exiting loop."
        break
    fi

    mapfile -t lines < "$file"
    for line in "${lines[@]}"; do
        echo "$line"
        array=(${line//__/ })
        depname=${array[0]}
        depversion=${array[1]}
        cd TestCollection
        git clone $repoUrl $projectName
        cd $projectName
        git checkout $commit
        cp "../../Playground/"$projectName"/package-lock.json" ./
        # git clone repo to temp folder, remove one direct dependency, run test, log, remove repo
        
        # exclude dep from the lock file
        python3 ../../scripts/exclude_indirect_dep.py $depname $depversion $projectName

        npm install

        echo "I am running test after removing the set of "$projectName" ....."
        # npm run test
        command_output=$(npm run test 2>&1)
        if [[ $command_output == *$testPassSignal* ]]; then
            echo $projectName","$line",1" >> ../../test_passed_result_output5.txt
        else
            echo $projectName","$line",0" >> ../../test_passed_result_output_error5.txt
        fi
        cd ..
        rm -rf $projectName
        cd ..
    done
done