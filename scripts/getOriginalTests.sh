jsonlist=$(jq -r '.projects' "repoPro.json")

# inside the loop, you cant use the fuction _jq() to get values from each object.
for row in $(echo "${jsonlist}" | jq -r '.[] | @base64')
do
    _jq()
    {
        echo ${row} | base64 --decode | jq -r ${1}
    }

    repoUrl=$(_jq '.gitURL')
    projectName=$(_jq '.folder')
    commit=$(_jq '.commit')

    echo $repoUrl 
    echo $projectName 
    echo $commit
    
    cd Original
    
    git clone $repoUrl

    cd $projectName
    
    git checkout $commit

    npm install

    echo "Start Generating test coverage report..."

    nyc npm run test

    cd ..
done
