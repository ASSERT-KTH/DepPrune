jsonlist=$(jq -r '.projects' "repos_733.json")

# inside the loop, you cant use the fuction _jq() to get values from each object.
for row in $(echo "${jsonlist}" | jq -r '.[] | @base64')
do
    _jq()
    {
        echo ${row} | base64 --decode | jq -r ${1}
    }

    repoUrl=$(_jq '.gitURL')
    projectName=$(_jq '.folder')
    repo=$(_jq '.repo')

    echo "I am package "$repo" ....."
    echo "I am package "$repo" ....." >> /dev/stderr
    
    cd TestCollection
    
    git clone $repoUrl $projectName

    cd $projectName

    cp 
    
    npm install

    echo "Start Generating test coverage report..."

    nyc npm run test

    cd ..
    rm -rf $projectName
    cd ..
done
