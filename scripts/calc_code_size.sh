jsonlist=$(jq -r '.projects' "repos_92_copy.json")
basement="Playground"
locations="direct_offspring_removed.txt"

for row in $(echo "${jsonlist}" | jq -r '.[] | @base64')
do
    _jq()
    {
        echo ${row} | base64 --decode | jq -r ${1}
    }
    repo=$(_jq '.repo')
    projectName=$(_jq '.folder')

    location_file=$basement"/"$projectName"/$locations"
    initial=0

    if [ -f "$location_file" ]; then
        mapfile -t location_lines < "$location_file"
        for line in "${location_lines[@]}"; do
            result=$(du -sk $basement"/"$projectName"/"$line | cut -f1)
            initial=$((initial + result))
        done
    fi


    
    echo $projectName","$initial
done
