# jsonlist=$(jq -r '.projects' "repos_93.json")
jsonlist=$(jq -r '.projects' "repos_demo.json")

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
    echo "I am package "$repoUrl" ....."  >> /dev/stderr

    file="../../Playground/"$projectName"/direct_confirmed_deps.txt"
    indirect_file="../../Playground/"$projectName"/individual_confirmed_only_runtime.txt"


    cd DebloatedPackages
    git clone $repoUrl $projectName
    cd $projectName

    git checkout $commit
    # rm -rf node_modules
    # rm -rf package-lock.json
    cp "../../LockFiles/"$projectName"/package-lock.json" ./
    # cp "../../LockFiles/"$projectName"/package-lock.json" ./package-lock-debloated.json
    

    mapfile -t lines < "$file"

    if [ "${#lines[@]}" -eq 0 ]; then
        echo "No direct bloated deps. Exiting loop."
    
    else
        echo "Removing direct dependency "$depname" in the package "$projectName
        # echo "Removing direct dependency "$depname" in the package "$projectName >> /dev/stderr
        python3 ../../modify_pkgjson.py $projectName "DebloatedPackages"
        # cp package.json ./package-debloated.json
    fi

    mapfile -t indirect_lines < "$indirect_file"
    if [ "${#indirect_lines[@]}" -eq 0 ]; then
        echo "No indirect bloated deps. Exiting loop."
        break
    else
        echo "Before removing sets in the package "$projectName" ....."
        # echo "Before removing sets in the package "$projectName" ....."  >> /dev/stderr
        python3 ../../exclude_entire_deps.py $projectName "DebloatedPackages"
    fi


    npm install

    echo "I am running test after removing the set of "$projectName" ....."
    echo "I am running test after removing the set of "$projectName" ....." >> /dev/stderr
    
    npm run test
    # command_output=$(npm run test 2>&1)
    # echo $command_output >> ../../test_entire_output.txt
    
    # npm run test
    # if [ $? -eq 0 ]; then
    #     echo $projectName","$line",1" >> ../test_output1_0.txt
    # else
    #     echo $projectName","$line",0" >> ../test_output_error1_0.txt
    # fi

    npm list --all --omit=dev > npm_list_output.txt
    grep -v "deduped" npm_list_output.txt > debloated_npm_list_filtered.txt
    cd ..
    rm -rf $projectName
    cd ..
done