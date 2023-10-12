jsonlist=$(jq -r '.projects' "repos.json")

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

    file="./Playground/"$projectName"/direct_unreachable.txt"

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
        cp "../../LockFiles/"$projectName"/package-lock.json" ./
        npm install
        echo "Before removing dependency "$depname" in the package "$projectName
        npm uninstall $depname

        echo "I am running test after removing the set of "$projectName" ....."
        # npm run test
        command_output=$(npm run test 2>&1)
        if [[ $command_output == *$testPassSignal* ]]; then
            echo $projectName","$line",1" >> ../test_output.txt
        else
            echo $projectName","$line",0" >> ../test_output_error.txt
        fi

        npm run test
        if [ $? -eq 0 ]; then
            echo $projectName","$line",1" >> ../test_output1.txt
        else
            echo $projectName","$line",0" >> ../test_output_error1.txt
        fi
        cd ..
        # rm -rf $projectName
        cd ..
    done
done