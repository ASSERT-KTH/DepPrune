jsonlist=$(jq -r '.projects' "repos_test.json")

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

    echo $repoUrl 
    echo $entryFile 
    echo $folderPath 
    echo $projectName 
    echo $commit


    # rm -rf $folderPath
    
    # git clone $repoUrl $folderPath

    # cd $folderPath
    
    # git checkout $commit

    # cd ../..

    # ./resetProject.sh $folderPath

    # python3 genDepList.py $folderPath "npm install "

    # python3 genNycRc.py $folderPath "${folderPath}/dep_list.txt" 
    
    cd $folderPath

    echo "Start Generating test coverage report..."

    nyc npm run test

    cd ../..

    echo "Start discovering bloated files..."

    ./transform.sh $folderPath "dynamic" false

    python3 scripts/extract_unreachable_deps.py $projectName 

    node scripts/dep-tree.js $folderPath $entryFile
    
done
