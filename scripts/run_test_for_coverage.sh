# path='./Logs/rerun_test_github_test.txt'
path='./Logs/rerun_test_coverage_test.txt'
cat $path | while read rows
do
   
    cd TestCollection
    array=(${rows//,/ })
    repo=${array[1]}
    echo "I am package "$repo" ....."
    echo "I am package "$repo" ....." >> /dev/stderr
    substring="/"
    folder="${repo#*$substring}"
    echo $folder
    giturl=${array[10]}
    echo $giturl

  
    git clone $giturl $folder
    cd $folder
    npm install

    echo "I am running test for "$repo""
    echo "I am running test for "$repo"" >> /dev/stderr
    nyc npm run test
    cd ..
    rm -rf $folder
    cd ..

done
