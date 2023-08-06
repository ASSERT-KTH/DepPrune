jsonlist=$(jq -r '.projects' "repos_70_copy.json")

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
    # echo "I am package "$repo" ....." >> /dev/stderr

    cd $folderPath
    # touch direct_bloated_deps_comp.txt
    # touch direct_bloated_deps_pseudo.txt
    touch direct_indirect_bloated_deps.txt
    # npm list --all --omit=dev > npm_list_output.txt
    cd ../..
    # python3 scripts/fetch_deduped_directs.py $folder
    
done