jsonlist=$(jq -r '.projects' "repo.json")

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
    testFolder="TestAfterRemoveFolders/"$(_jq '.folder')
    unitTest=$(_jq '.unitTest')

    echo $folderPath 

    cp -r $folderPath $testFolder

    cd $testFolder

    file="../../Playground/"$projectName"/unreachable_runtime_deps_removed.txt"
    mapfile -t lines < "$file"

    for line in "${lines[@]}"; do
        echo $line
        rm -rf $line
    done
    npm run $unitTest
    cd ../..

done
