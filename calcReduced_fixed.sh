# jsonlist=$(jq -r '.projects' "repos_92_test.json")
jsonlist=$(jq -r '.projects' "repos_fix.json")

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

    non_bloated_file="Playground/"$projectName"/non-bloated_deps_location_dedup.txt"
    initial=0
    # echo "I am package "$repo" ....."

    mapfile -t non_bloated_lines < "$non_bloated_file"
    for non_bloated in "${non_bloated_lines[@]}"; do
        result=$(du -sk "Playground/"$projectName"/"$non_bloated | cut -f1)
        initial=$((initial + result))
    done

    
    echo $projectName","$initial
done
