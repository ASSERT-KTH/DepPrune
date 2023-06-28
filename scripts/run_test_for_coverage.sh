# path='./Logs/rerun_test_github_test.txt'
path='./Logs/rerun_test_1000_commits_waiting_copy.txt'
path_done='./Logs/rerun_test_1000_commits_waiting_done.txt'

sort "$path" -o "$path"
sort "$path_done" -o "$path_done"

diff_lines=$(comm -23 "$path" "$path_done")

diff_array=()
while IFS= read -r line; do
  diff_array+=("$line")
done <<< "$diff_lines"

echo ${#diff_array[@]}

# cat $path | while read rows
for rows in ${diff_array[@]};
do
    echo "$rows" >> ./Logs/rerun_test_1000_commits_waiting_done.txt
    cd TestCollection
    array=(${rows//,/ })
    repo=${array[1]}
    echo "I am package "$repo" ....."
    echo "I am package "$repo" ....." >> /dev/stderr
    substring="/"
    folder="${repo#*$substring}"
    giturl="https://github.com/"$repo".git"
  
    git clone $giturl $folder
    cd $folder
    npm install

    echo "I am running test for "$repo""
    echo "I am running test for "$repo"" >> /dev/stderr
    timeout -k 10s 5m nyc npm run test
    cd ..
    rm -rf $folder
    cd ..

done
