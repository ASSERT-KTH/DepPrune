jsonlist=$(jq -r '.projects' "repos_70.json")

# inside the loop, you cant use the fuction _jq() to get values from each object.
for row in $(echo "${jsonlist}" | jq -r '.[] | @base64')
do
    _jq()
    {
        echo ${row} | base64 --decode | jq -r ${1}
    }
    giturl=$(_jq '.gitURL')
    repo=$(_jq '.repo')
    folder=$(_jq '.folder')
    folderPath="Playground/"$(_jq '.folder')

    echo "I am package "$repo" ....."
    echo "I am package "$repo" ....." >> /dev/stderr
    file="./Playground/"$folder"/direct_bloated_deps_comp.txt"
    file1="../../Playground/"$folder"/direct_bloated_deps_comp.txt"
    
    if [ -s $file ]; then
        cd TestCollection
        git clone $giturl $folder
        cd $folder
        git checkout $commit
        cp "../../Playground/"$folder"/package-lock.json" ./package-lock.json
        npm install

        echo "Before removing completely bloated direct deps in the package "$folder
        echo "Before removing completely bloated direct deps in the package "$folder >> /dev/stderr

        mapfile -t lines < "$file1"

            for line in "${lines[@]}"; do
            echo "$line"
            array=(${line//__/ })
            depname=${array[0]}
            depversion=${array[1]}
            echo $depname
            
            npm uninstall $depname
            done

        echo "After removing completely bloated direct deps in the package "$folder
        echo "After removing completely bloated direct deps in the package "$folder >> /dev/stderr
        npm run test
        cd ..
        rm -rf $folder
        cd ..
    else
        echo "The file is empty."
    fi
done