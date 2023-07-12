path='Logs/target_69_packages_loc.txt'
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

    file="./Playground/"$folder"/bloated_direct_deps.txt"

    mapfile -t lines < "$file"

    for line in "${lines[@]}"; do
        echo "$line"
        # git clone repo to temp folder, remove one direct dependency, run test, log, remove repo
        cd TestCollection
        git clone $giturl $folder
        cd $folder
        git checkout $commit
        cd ../..
        pckjson="TestCollection/"$folder"/package.json"
        echo "Remove dependency "$line" in the package "$folder
        echo "Remove dependency "$line" in the package "$folder >> /dev/stderr
        python3 scripts/remove_one_dependency.py $pckjson $line
        cd TestCollection
        cd $folder
        npm install
        echo $folder","$line",$(( $(npm list --all --omit=dev | wc -l) - 1 ))" >> "../../output_deps_size.txt"
        npm run test
        cd ..
        rm -rf $folder
        cd ..
    done

    # echo "$(npm list --all --omit=dev | wc -l)" >> "../../output_deps_size.txt"
    # cd ../..
    # python3 scripts/extract_empty_files.py $folder
    # python3 scripts/remove_duplicates.py "Playground/"$folder"/bloated_deps_physical_level.txt"
done