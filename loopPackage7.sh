jsonlist=$(jq -r '.projects' "repos_92.json")

# inside the loop, you cant use the fuction _jq() to get values from each object.
for row in $(echo "${jsonlist}" | jq -r '.[] | @base64')
do
    _jq()
    {
        echo ${row} | base64 --decode | jq -r ${1}
    }
    repoUrl=$(_jq '.gitURL')
    entryFile=$(_jq '.entryFile')
    projectName=$(_jq '.folder')
    folderPath="Playground/"$(_jq '.folder')
    commit=$(_jq '.commit')

    # echo $repoUrl 
    echo $folderPath 

    # rm -rf "${folderPath}/non-isolated-clients.json"
    rm -rf "${folderPath}/direct-isolated-deps.txt"
    # rm -rf "${folderPath}/direct_bloated_deps_pseudo.txt"
    # rm -rf "${folderPath}/direct_bloated_deps_comp.txt"
    
    
    
done
