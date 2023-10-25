jsonlist=$(jq -r '.projects' "repo.json")
basement="Playground"
locations="bloated_locations.txt"

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

    mapfile -t location_lines < "$location_file"
    for line in "${location_lines[@]}"; do
        result=$(du -sk $basement"/"$projectName"/"$line | cut -f1)
        initial=$((initial + result))
    done

    
    echo $projectName","$initial
done
