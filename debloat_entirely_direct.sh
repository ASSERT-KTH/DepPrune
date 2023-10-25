jsonlist=$(jq -r '.projects' "repos_93.json")

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

    cd DirectDebloated
    git clone $repoUrl $projectName
    cd $projectName

    git checkout $commit
    cp "../../DebloatedPackages/"$projectName"/package.json" ./
    

    mapfile -t lines < "$file"

    if [ "${#lines[@]}" -eq 0 ]; then
        echo "No direct bloated deps. Exiting loop."
    
    else
        for line in "${lines[@]}"; do
            echo "Removing direct dependency "$line" in the package "$projectName
            echo "Removing direct dependency "$line" in the package "$projectName >> /dev/stderr
            array=(${line//__/ })
            depname=${array[0]}
            echo "Removing direct dependency "$depname" in the package "$projectName >> /dev/stderr
            npm uninstall $depname
        done
    fi

    npm install

    echo "I am running test after removing the set of "$projectName" ....."
    echo "I am running test after removing the set of "$projectName" ....." >> /dev/stderr
    npm list --all --omit=dev > direct_npm_list_output.txt
    grep -v "deduped" direct_npm_list_output.txt > direct_debloated_npm_list_filtered.txt
    npm run test
    
    cd ../..
done