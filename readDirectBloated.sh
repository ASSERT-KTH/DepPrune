jsonlist=$(jq -r '.projects' "repoDirect.json")

# inside the loop, you cant use the fuction _jq() to get values from each object.
for row in $(echo "${jsonlist}" | jq -r '.[] | @base64')
do
    _jq()
    {
        echo ${row} | base64 --decode | jq -r ${1}
    }
    repoUrl=$(_jq '.gitURL')
    entryFile=$(_jq '.entryFile')
    project=$(_jq '.folder')
    folderPath="DirectBloated/"$(_jq '.folder')
    dataFolderPath="Data/"$(_jq '.folder')
    projectName=$(_jq '.folder')
    commit=$(_jq '.commit')

    echo $repoUrl 
    echo $entryFile 
    echo $folderPath 
    echo $projectName 
    echo $commit

    # cd DirectBloated
    # mkdir $projectName
    # cd ..

    # rm -rf $folderPath
    
    # git clone $repoUrl $folderPath

    cd $folderPath
    
    # git checkout $commit

    # npm install

    # npm run test

    npm list --all --omit=dev --json >> "../../Data/"$project"/productionDependencies_withoutBloat.json"

    cd ../..
done
