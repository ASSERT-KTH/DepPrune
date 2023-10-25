jsonlist=$(jq -r '.projects' "repo.json")

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

    direct_file="../../Playground/"$projectName"/direct_confirmed_deps.txt"
    indirect_file="../../Playground/"$projectName"/individual_confirmed_only_runtime.txt"


    cd DebloatedPackages
    git clone $repoUrl $projectName
    cd $projectName

    git checkout $commit
    cp "../../LockFiles/"$projectName"/package-lock.json" ./
    

    mapfile -t lines < "$direct_file"

    if [ "${#lines[@]}" -eq 0 ]; then
        echo "No direct bloated deps. Exiting loop."
    
    else
        for line in "${lines[@]}"; do
            echo "Removing direct dependency "$line" in the package "$projectName
            array=(${line//__/ })
            depname=${array[0]}
            echo "Removing direct dependency "$depname" in the package "$projectName >> /dev/stderr
            npm uninstall $depname
        done
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
    # echo "I am running test after removing the set of "$projectName" ....." >> /dev/stderr
    
    npm run test

    npm list --all --omit=dev > npm_list_output.txt
    grep -v "deduped" npm_list_output.txt > debloated_npm_list_filtered.txt
    cd ../..
done