jsonlist=$(jq -r '.projects' "repos_93.json")
# jsonlist=$(jq -r '.projects' "repos_temp.json")
basement="Playground"
# basement="TestCollectionEntire"
# inside the loop, you cant use the fuction _jq() to get values from each object.
for row in $(echo "${jsonlist}" | jq -r '.[] | @base64')
do
    _jq()
    {
        echo ${row} | base64 --decode | jq -r ${1}
    }
    repo=$(_jq '.repo')
    projectName=$(_jq '.folder')

    location_file=$basement"/"$projectName"/all_bloated_deps_location_size.txt"
    initial=0
    # echo "I am package "$repo" ....."

    mapfile -t location_lines < "$location_file"
    for line in "${location_lines[@]}"; do
        result=$(du -sk $basement"/"$projectName"/"$line | cut -f1)
        initial=$((initial + result))
    done

    
    echo $projectName","$initial
done
