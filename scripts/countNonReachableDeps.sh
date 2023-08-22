jsonlist=$(jq -r '.projects' "repos_92.json")

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

    # echo "I am package "$repo" ....."

    cd Playground
    cd $folder
    result_temp=$(($(wc -l < original_npm_list_filtered.txt) - 2))
    unmet=$(grep -c "UNMET" original_npm_list_filtered.txt)
    # reachable=$(wc -l < reachable-deps.txt)
    result=$(($result_temp - $unmet))
    echo $folder","$result

    cd ../..
done