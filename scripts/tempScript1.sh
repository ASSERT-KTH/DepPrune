path='Logs/target_9_packages.txt'
cat $path | while read rows
do
    # echo "I am package "$rows" ....."
    # python3 collectDependentFiles.py $rows
    # echo "I am package "$rows" ....." >> /dev/stderr
    cd Original
    array=(${rows//,/ })
    folder=${array[0]}
    giturl=${array[11]}
    cd $folder
    echo "I am package "$folder" ....."
    git clone $giturl $folder
    # npm install
    # cd $folder
    cd ..

done