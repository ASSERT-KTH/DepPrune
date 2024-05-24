#!/bin/bash
jsonlist=$(jq -r '.projects' "repos.json")

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
    testFolder="TestAfterRemove_Stubbifier/"$(_jq '.folder')
    unitTest=$(_jq '.unitTest')
    testPassSignal=$(_jq '.testPassSignal')

    echo "I am package "$folderPath 


    file="Playground/"$projectName"/stubbifier_misclassified.txt"

    mapfile -t lines < "$file"
    for line in "${lines[@]}"; do
        echo $line
        mkdir $testFolder
        
        # clone from the original package
        rsync -av --exclude='*.txt' 'Playground/'$projectName TestAfterRemove_Stubbifier

        cd $testFolder
        rm -rf $line

        command_output=$(npm run $unitTest 2>&1)
        
        if [[ $command_output == *$testPassSignal* ]]; then
            echo $projectName","$line",1" >> ../../test_output.txt
        else
            echo $projectName","$line",0" >> ../../test_output_error.txt
        fi

        # npm run $unitTest
        # if [ $? -eq 0 ]; then
        #     echo $projectName","$line",1" >> ../../test_output1.txt
        # else
        #     echo $projectName","$line",0" >> ../../test_output_error1.txt
        # fi
        cd ../..
        rm -rf $testFolder

    done
done
