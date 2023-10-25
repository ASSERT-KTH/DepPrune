jsonlist=$(jq -r '.projects' "repo.json")
basement="Playground"
analyzed_deps="direct_unreachable.txt"

for row in $(echo "${jsonlist}" | jq -r '.[] | @base64')
do
    _jq()
    {
        echo ${row} | base64 --decode | jq -r ${1}
    }
    repo=$(_jq '.repo')
    projectName=$(_jq '.folder')

    dep_file=$basement"/"$projectName"/$analyzed_deps"
    exclude_folder=$basement"/"$projectName"/node_modules"

    mapfile -t lines < "$dep_file"
    for line in "${lines[@]}"; do
        array=(${line//__/ })
        dependency=${array[0]}
        echo "I am the "$dependency" in the package "$projectName
        find $basement"/"$projectName -type f -name "*.js" -not -path "$exclude_folder/*" -exec grep -H $dependency {} +
    done
done
