jsonlist=$(jq -r '.projects' "repos_temp.json")

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
    echo "I am package "$repoUrl" ....." >> /dev/stderr

    # file="./Playground/"$projectName"/isolated_passed_deps.txt"

    # mapfile -t lines < "$file"
    # if [ $lines -eq 0 ]; then
    #     echo "No deps. Exiting loop."
    #     break
    # fi

    cd TestCollection
    git clone $repoUrl $projectName
    cd $projectName
    git checkout $commit
    cp "../../Playground/"$projectName"/package-lock.json" ./
    python3 ../../scripts/exclude_indirect_dep_in_set.py $projectName
    npm install

    echo "I am running test after removing set of "$projectName" ....."
    echo "I am running test after removing set of "$projectName" ....." >> /dev/stderr

    npm run test
    # command_output=$(npm run test 2>&1)
    # if [[ $command_output == *$testPassSignal* ]]; then
    #     echo $projectName","$line",1" >> ../../test_indirect_result_output1.txt
    # else
    #     echo $projectName","$line",0" >> ../../test_indirect_result_output_error1.txt
    # fi
    cd ..
    rm -rf $projectName
    cd ..
done