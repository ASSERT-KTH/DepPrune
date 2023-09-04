# jsonlist=$(jq -r '.projects' "repos_92_test.json")
jsonlist=$(jq -r '.projects' "repos_temp.json")

# inside the loop, you cant use the fuction _jq() to get values from each object.
for row in $(echo "${jsonlist}" | jq -r '.[] | @base64')
do
    _jq()
    {
        echo ${row} | base64 --decode | jq -r ${1}
    }
    giturl=$(_jq '.gitURL')
    repo=$(_jq '.repo')
    projectName=$(_jq '.folder')
    folderPath="Playground/"$(_jq '.folder')
    commit=$(_jq '.commit')

    direct_confirmed_file="../../Playground/"$projectName"/direct_confirmed_deps.txt"
    indirect_confirmed_file="../../Playground/"$projectName"/indirect_confirmed_deps.txt"

    echo "I am package "$repo" ....."
    echo "I am package "$repo" ....." >> /dev/stderr

    cd TestCollection
    git clone $giturl $projectName
    cd $projectName
    git checkout $commit
    cp "../../Playground/"$projectName"/package-lock.json" ./

    npm install
    npm list --all --omit=dev > npm_list_output_before.txt
    grep -v "deduped" npm_list_output_before.txt > npm_list_filtered_output_before.txt
    resultbefore_temp=$(($(wc -l < npm_list_filtered_output_before.txt) - 2))
    unmet=$(grep -c "UNMET" npm_list_filtered_output_before.txt)
    resultbefore=$(($resultbefore_temp - $unmet))
    echo $projectName" resultbefore: "$resultbefore
    echo $projectName" resultbefore: "$resultbefore >> /dev/stderr


    # npm install --omit=dev
    # resultbefore=$(du -sk node_modules | cut -f1)
    # echo $projectName" resultbefore: "$resultbefore
    # echo $projectName" resultbefore: "$resultbefore >> /dev/stderr

    
    if [ -f $direct_confirmed_file ]; then
        echo $projectName" direct confirmed exists"
        mapfile -t direct_lines < "$direct_confirmed_file"
        for direct in "${direct_lines[@]}"; do
            # echo "npm uninstall $direct"
            di_array=(${direct//__/ })
            depname=${di_array[0]}
            depversion=${di_array[1]}
            npm uninstall $depname
        done
    fi

    # echo "Run test after removing direct deps in the package "$projectName
    # echo "Run test after removing direct deps in the package "$projectName >> /dev/stderr
    # # npm run test


    mapfile -t indirect_lines < "$indirect_confirmed_file"
    for indirect in "${indirect_lines[@]}"; do
        # echo "npm modify lock file by $indirect"
        in_array=(${indirect//__/ })
        depname=${in_array[0]}
        depversion=${in_array[1]}
        # exclude dep from the lock file
        python3 ../../scripts/exclude_indirect_dep.py $depname $depversion $projectName 
    done

    rm -rf node_modules
    # npm install --omit=dev
    # resultafter=$(du -sk node_modules | cut -f1)
    # echo $projectName" resultafter: "$resultafter
    # echo $projectName" resultafter: "$resultafter >> /dev/stderr
    
    npm install
    echo "Run test after removing indirect deps in the package "$projectName
    echo "Run test after removing indirect deps in the package "$projectName >> /dev/stderr
    npm run test

    npm list --all --omit=dev > npm_list_output_after.txt
    grep -v "deduped" npm_list_output_after.txt > npm_list_filtered_output_after.txt
    resultafter_temp=$(($(wc -l < npm_list_filtered_output_after.txt) - 2))
    unmet2=$(grep -c "UNMET" npm_list_filtered_output_after.txt)
    resultafter=$(($resultafter_temp - $unmet2))
    echo $projectName" resultafter: "$resultafter
    echo $projectName" resultafter: "$resultafter >> /dev/stderr

    cd ..
    # rm -rf $projectName
    cd ..

done
