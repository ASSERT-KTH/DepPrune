jsonlist=$(jq -r '.projects' "repos_70.json")

# inside the loop, you cant use the fuction _jq() to get values from each object.
for row in $(echo "${jsonlist}" | jq -r '.[] | @base64')
do
    _jq()
    {
        echo ${row} | base64 --decode | jq -r ${1}
    }
    giturl=$(_jq '.gitURL')
    repo=$(_jq '.repo')
    folder=$(_jq '.folder')
    folderPath="Playground/"$(_jq '.folder')

    echo "I am package "$repo" ....."
    echo "I am package "$repo" ....." >> /dev/stderr

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
        echo "Before removing dep "$line" in the package "$folder
        echo "Before removing dep "$line" in the package "$folder >> /dev/stderr
        npm install
         
        npm list --all --omit=dev > npm_list_output_before.txt
        grep -v "deduped" npm_list_output_before.txt > npm_list_filtered_output_before.txt
        resultbefore=$(($(wc -l < npm_list_filtered_output_before.txt) - 2))

        echo "Deps size of "$depname"__"$folder" before removal is "$resultbefore
        echo "Deps size of "$depname"__"$folder" before removal is "$resultbefore >> /dev/stderr
        
        # python3 scripts/calc_code_size.py $folder True
        
        npm uninstall $depname
        
        echo "After removing dep "$line" in the package "$folder
        echo "After removing dep "$line" in the package "$folder >> /dev/stderr

        npm list --all --omit=dev > npm_list_output_after.txt
        grep -v "deduped" npm_list_output_after.txt > npm_list_filtered_output_after.txt
        resultafter=$(($(wc -l < npm_list_filtered_output_after.txt) - 2))
        
        echo "Deps size of "$depname"__"$folder" after removal is "$resultafter
        echo "Deps size of "$depname"__"$folder" after removal is "$resultafter >> /dev/stderr

        # python3 scripts/calc_code_size.py $folder False
        npm run test
        cd ..
        rm -rf $folder
        cd ..
    done
done