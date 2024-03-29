jsonlist=$(jq -r '.projects' "repos_92.json")

for row in $(echo "${jsonlist}" | jq -r '.[] | @base64')
do
    _jq()
    {
        echo ${row} | base64 --decode | jq -r ${1}
    }
    repoUrl=$(_jq '.gitURL')
    projectName=$(_jq '.folder')
    folderPath="Playground/"$(_jq '.folder')
    commit=$(_jq '.commit')
    unitTest=$(_jq '.unitTest')

    # echo $repoUrl 
    echo $folderPath 
    
    mkdir "stubbifier/Playground/"$projectName
    # copy the packages in our dataset, exclude the .txt files, exclude /node_modules
    # rsync -av --exclude='*.txt' --exclude='node_modules/' --exclude='coverage/' 'Playground/'$projectName 'stubbifier/Playground/'

    git clone $repoUrl "stubbifier/Playground/"$projectName
    cp 'Playground/'$projectName'/package-lock.json' "stubbifier/Playground/"$projectName

    cd stubbifier

    echo -n "" > Playground/all_files_in_stubbifier.txt
    echo -n "" > Playground/stubbifier_bloated_candidates.txt

    # start running stubbifier
    # # # # # # # # # # # # # # # # # # # # # # # 
    ./resetProject.sh Playground/$projectName
    python3 genDepList.py Playground/$projectName "npm install "
    python3 genNycRc.py Playground/$projectName Playground/$projectName/dep_list.txt
    cd Playground/$projectName
    nyc npm run $unitTest 
    cd ../..
    ./transform.sh Playground/$projectName "dynamic" false
    # # # # # # # # # # # # # # # # # # # # # # # 
    # end running stubbifier
    
    cp Playground/all_files_in_stubbifier.txt 'Playground/'$projectName'_all_files_in_stubbifier'.txt
    cp Playground/stubbifier_bloated_candidates.txt 'Playground/'$projectName'_stubbifier_bloated_candidates'.txt

    cd ..

    python3 extract_difference.py $projectName "all_files_in_stubbifier.txt" "stubbifier_bloated_candidates.txt" "stubbifier_accessed_files.txt"

done