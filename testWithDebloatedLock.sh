#!/bin/bash
jsonlist=$(jq -r '.projects' "repo.json")

for row in $(echo "${jsonlist}" | jq -r '.[] | @base64')
do
    _jq()
    {
        echo ${row} | base64 --decode | jq -r ${1}
    }
    repoUrl=$(_jq '.gitURL')
    # entryFile=$(_jq '.entryFile')
    projectName=$(_jq '.folder')
    folderPath="Playground/"$(_jq '.folder')
    testFolder="TestWithDebloatedLock/"$(_jq '.folder')
    commit=$(_jq '.commit')
    unitTest=$(_jq '.unitTest')

    # # echo $repoUrl 
    echo $projectName 
    
    git clone $repoUrl $testFolder

    cd $testFolder

    git checkout $commit

    rm -rf package.json

    cp "../../DebloatedLocks/${projectName}/package.json" ./
    cp "../../DebloatedLocks/${projectName}/package-lock.json" ./

    npm install

    cd ../..

    python3 checkBloatedExists.py $projectName

    cd $testFolder
    npm run $unitTest
    cd ../..
    
done
