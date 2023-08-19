path='Logs/target_70_packages_copy.txt'
cat $path | while read rows
do
    # echo "I am package "$rows" ....."
    # python3 collectDependentFiles.py $rows
    # echo "I am package "$rows" ....." >> /dev/stderr
    array=(${rows//,/ })
    folder=${array[0]}
    repo=${array[1]}
    commit=${array[9]}
    giturl=${array[12]}
    # cd Original
    # cd $folder
    
    echo "I am package "$repo" ....."
    echo "I am package "$repo" ....." >> /dev/stderr

    # cd TestCollection
    # git clone $giturl $folder
    # cd $folder
    # git checkout $commit
    # npm install
    # originalsize=$(( $(npm list --all --omit=dev | wc -l) - 2 ))
    # echo "original size: "$originalsize
    # cd ..
    # rm -rf $folder
    # cd ..

    file="./Playground/"$folder"/direct_bloated_deps.txt"

    mapfile -t lines < "$file"

    for line in "${lines[@]}"; do
        echo "$line"
        array=(${line//__/ })
        depname=${array[0]}
        depversion=${array[1]}
        echo $depname
        # git clone repo to temp folder, remove one direct dependency, run test, log, remove repo
        cd TestCollection
        git clone $giturl $folder
        cd $folder
        git checkout $commit
        cp "../../Playground/"$folder"/package-lock.json" ./package-lock.json
        echo "Before removing dependency "$depname" in the package "$folder
        echo "Before removing dependency "$depname" in the package "$folder >> /dev/stderr
        npm install
         
        npm list --all --omit=dev > npm_list_output_before.txt
        grep -v "deduped" npm_list_output_before.txt > npm_list_filtered_output_before.txt
        resultbefore=$(($(wc -l < npm_list_filtered_output_before.txt) - 2))

        echo "Result of deps size of "$depname","$folder" before is "$resultbefore
        echo "Result of deps size of "$depname","$folder" before is "$resultbefore >> /dev/stderr
        
        # python3 scripts/calc_code_size.py $folder True
        
        npm uninstall $depname
        
        npm list --all --omit=dev > npm_list_output_after.txt
        grep -v "deduped" npm_list_output_after.txt > npm_list_filtered_output_after.txt
        resultafter=$(($(wc -l < npm_list_filtered_output_after.txt) - 2))
        echo "After removing dependency "$line" in the package "$folder
        echo "After removing dependency "$line" in the package "$folder >> /dev/stderr
        echo "Result of deps size of "$depname","$folder" after is "$resultafter
        echo "Result of deps size of "$depname","$folder" after is "$resultafter >> /dev/stderr

        # python3 scripts/calc_code_size.py $folder False
        npm run test
        cd ..
        rm -rf $folder
        cd ..
    done

    # echo "$(( $(npm list --all --omit=dev | wc -l) - 2 ))" >> "../../output_deps_size.txt"
    # cd ../..
    # python3 scripts/extract_empty_files.py $folder
    # python3 scripts/remove_duplicates.py "Playground/"$folder"/bloated_deps_physical_level.txt"
done