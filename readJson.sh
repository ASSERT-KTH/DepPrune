jsonlist=$(jq -r '.projects' "repoSet.json")

# mkdir VariantsDep
mkdir VariantsSubtree
# mkdir VariantsFile

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
    folderPath="Playground/"$(_jq '.folder')
    projectName=$(_jq '.folder')
    commit=$(_jq '.commit')

    echo $repoUrl 
    echo $entryFile 
    echo $folderPath 
    echo $projectName 
    echo $commit


    cd VariantsSubtree
    mkdir $projectName
    cd ..

    # cd VariantsDep
    # mkdir $projectName
    # cd ..

    # cd VariantsFile
    # mkdir $projectName
    # cd ..

    # rm -rf $folderPath
    
    # git clone $repoUrl $folderPath

    # cd $folderPath
    
    # git checkout $commit

    # cd ../..

    # ./resetProject.sh $folderPath

    # python3 genDepList.py $folderPath "npm install "

    # python3 genNycRc.py $folderPath "${folderPath}/dep_list.txt" 
    
    # cd $folderPath

    # echo "Start Generating test coverage report..."

    # nyc npm run test

    # cd ../..

    # echo "Start discovering bloated files..."

    # ./transform.sh $folderPath "dynamic" false

    # npm install --save dependency-tree

    # node dep-tree.js $folderPath $entryFile

    node generate-variant.js  $folderPath $projectName $repoUrl $commit

    node generate-variant-subtree.js  $folderPath $projectName $repoUrl $commit

    # node generate-variant-pureDep.js  $folderPath $projectName $repoUrl $commit

    # node generate-variant-file.js  $folderPath $projectName $repoUrl $commit

done
