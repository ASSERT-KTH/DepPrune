#!/bin/bash
jsonlist=$(jq -r '.projects' "repos_92_copy.json")
# TestFolder="TestCollection"

for row in $(echo "${jsonlist}" | jq -r '.[] | @base64')
do
    _jq()
    {
        echo ${row} | base64 --decode | jq -r ${1}
    }
    # repoUrl=$(_jq '.gitURL')
    # entryFile=$(_jq '.entryFile')
    projectName=$(_jq '.folder')
    folderPath="Playground/"$(_jq '.folder')
    # commit=$(_jq '.commit')
    unitTest=$(_jq '.unitTest')

    # # echo $repoUrl 
    # echo "I am package "$projectName 
    
    # mkdir "DebloatedLocks/${projectName}"

    # rm -rf "DebloatedLocks/${projectName}/package.json"
    # rm -rf "DebloatedLocks/${projectName}/package-lock.json"
    
    # cp "Playground/${projectName}/package.json" "DebloatedLocks/${projectName}"
    # cp "Playground/${projectName}/package-lock.json" "DebloatedLocks/${projectName}"


    
    # cd ../..
    # # extract the list of runtime dependencies
    # python3 identify_runtime_from_lock.py $projectName

    # echo $folderPath

    # echo "Start running test..."
    # cd $folderPath
    # # run test and trace open/openat .js/.json files at the OS level
    # strace -f -e trace=open,openat -o npm_test_trace.txt npm run $unitTest
    # # grep
    # grep -E "open\(|openat\(" npm_test_trace.txt | awk -F, '{print $2}' | grep "/${projectName}" | grep -E ".js\"$|.json\"$" | sort | uniq > "npm_test_opened_files.txt"


    # file="./Playground/"$projectName"/unreachable_runtime_deps.txt"

    # mapfile -t lines < "$file"

    # if [ $lines -eq 0 ]; then
    #     echo "No bloated deps. Exiting loop."
    #     break
    # fi

    # for line in "${lines[@]}"; do
    #     # copy the folder
    #     # remove the dep
    #     # run test, record the result
    #     # remove the folder
    #     echo "$line"
    #     cp -r "Playground/"$projectName "TestCollection/"$projectName
    #     rm -rf "TestCollection/"$projectName"/"$line
    #     cd "TestCollection/"$projectName

    #     echo "I am running test after removing the "$line" ....."
    #     # npm run $unitTest
    #     command_output=$(npm run test 2>&1)
    #     if [[ $command_output == *$testPassSignal* ]]; then
    #         echo $projectName","$line",1" >> ../test_output_0.txt
    #     else
    #         echo $projectName","$line",0" >> ../test_output_error_0.txt
    #     fi

    #     npm run test
    #     if [ $? -eq 0 ]; then
    #         echo $projectName","$line",1" >> ../test_output1_0.txt
    #     else
    #         echo $projectName","$line",0" >> ../test_output_error1_0.txt
    #     fi
    #     cd ..
    #     rm -rf $projectName
    #     cd ..
    # done
    

    
    # python3 extract_difference.py $projectName "unreachable_deps_stubbifier.txt" "unreachable_runtime_deps.txt" "bloated_in_stubbifier_not_in_os.txt"

        python3 extract_intersection.py $projectName "direct_location.txt" "bloated_in_stubbifier_not_in_os.txt" "false_positive_direct_stubbifier.txt"
    # rm -rf Playground/"$projectName"/bloated_in_os_accessed_in_stubbifier.txt

    # python3 extract_difference.py $projectName "unreachable_deps_stubbifier.txt" "unreachable_deps_stubbifier_removed.txt" "unreachable_deps_stubbifier_failed.txt"

    # python3 extract_intersection.py $projectName "unreachable_runtime_deps.txt" "unreachable_runtime_deps_nyc.txt" "unreachable_runtime_deps_both.txt"

    # folder_path="stubbifier/Playground/"$projectName"/coverage/"
    # file_to_copy="../CJS-Debloator/Playground/"$projectName"/coverage/coverage-final.json"

    # if [ -d "$folder_path" ]; then
    #     echo "Folder already exists."
    # else
    #     # If the folder doesn't exist, create it
    #     mkdir -p "$folder_path"
    #     echo "Folder created."
    # fi

    # cp ../CJS-Debloator/Playground/"$projectName"/coverage/coverage-final.json stubbifier/Playground/"$projectName"/coverage/

    # python3 handle_coverage.py $projectName
    # rm -rf Playground/"$projectName"/unreachable_deps_stubbifier.txt
    # rm -rf Playground/"$projectName"/stubbifier_accessed_deps.txt
    # python3 extract_bloated_candidates_stubbifier.py $projectName
    # python3 remove_duplicates.py "./Playground/"$projectName"/unreachable_deps_stubbifier.txt"


    # python3 debloat_pck_json.py $projectName
    # python3 debloat_lock_file.py $projectName
    # cd Playground/$projectName
    # npmlist=$(( $(npm list -prod -depth 15 | grep -v "extraneous" | wc -l) - 2 ))
    # echo $projectName","$npmlist
    # cd ../..

    # python3 temp.py $projectName
done
