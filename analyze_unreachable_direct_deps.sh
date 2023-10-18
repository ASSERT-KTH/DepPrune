jsonlist=$(jq -r '.projects' "repos_demo.json")
basement="Playground"

for row in $(echo "${jsonlist}" | jq -r '.[] | @base64')
do
    _jq()
    {
        echo ${row} | base64 --decode | jq -r ${1}
    }
    repo=$(_jq '.repo')
    projectName=$(_jq '.folder')

    direct_dep_file=$basement"/"$projectName"/direct_deps_only_runtime.txt"
    exclude_folder=$basement"/"$projectName"/node_modules"

    mapfile -t direct_lines < "$direct_dep_file"
    for line in "${direct_lines[@]}"; do
        array=(${line//__/ })
        dependency=${array[0]}
        echo "I am the "$dependency" in the package "$projectName
        find $basement"/"$projectName -type f -name "*.js" -not -path "$exclude_folder/*" -exec grep -H $dependency {} +
        # find "podcast-search" -type f -name "*.js" -exec grep -H "escape-string-regexp" {} +
    done
done
