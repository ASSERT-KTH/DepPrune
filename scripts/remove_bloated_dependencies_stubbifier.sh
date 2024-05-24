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

    echo "I am package "$folderPath 

    analyzer_output="True"

    while [ "$analyzer_output" = "True" ]
    do
        mkdir $testFolder
        
        # copy from the original packages
        # rsync -av --exclude='*.txt' 'Playground/'$projectName TestAfterRemove_Stubbifier
        # or git clone
        git clone $repoUrl $testFolder

        cd $testFolder

        cp "../../Playground/${projectName}/package-lock.json" ./

        npm ci

        file="../../Playground/"$projectName"/stubbifier_misclassified.txt"
        # if [ -e "$file" ]; then
        #     echo "File already exists."
        # else
        #     echo "File not exists."
        # fi

        mapfile -t lines < "$file"

        for line in "${lines[@]}"; do
            echo $line
            rm -rf $line
        done

        npm run $unitTest &>> "../../test_log.txt"
        cd ../..
        analyzer_output=$(python3 analyze_test_log.py $projectName)
        echo $analyzer_output
        rm -rf $testFolder
        echo -n "" > test_log.txt
    done
done
