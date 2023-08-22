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

    
    echo "I am package "$repoUrl" ....."
    echo $testPassSignal

    file="./Playground/"$projectName"/direct_bloated_deps.txt"

    mapfile -t lines < "$file"

    if [ $lines -eq 0 ]; then
        echo "No direct bloated deps. Exiting loop."
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
        npm install
        echo "Before removing dependency "$depname" in the package "$folder
        npm uninstall $depname
        echo "I am running test after removing dep "$line" ....."
        command_output=$(npm run test 2>&1)
        echo $command_output
        if [[ $command_output == *$testPassSignal* ]]; then
            echo $projectName","$line",1" >> ../../test_direct_result_output1.txt
        else
            echo $projectName","$line",0" >> ../../test_direct_result_output_error1.txt
        fi
        cd ..
        rm -rf $projectName
        cd ..
    done
done