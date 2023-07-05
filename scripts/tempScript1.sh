path='Logs/target_103_loc_loc_loc.txt'
cat $path | while read rows
do
    # echo "I am package "$rows" ....."
    # python3 collectDependentFiles.py $rows
    # echo "I am package "$rows" ....." >> /dev/stderr
    cd Original
    array=(${rows//,/ })
    folder=${array[0]}
    sha=${array[9]}
    giturl=${array[12]}
    
    echo "I am package "$folder" ....."
    git clone $giturl $folder
    cd $folder
    git checkout $sha
    npm install
    # cd $folder
    cd ../..

done