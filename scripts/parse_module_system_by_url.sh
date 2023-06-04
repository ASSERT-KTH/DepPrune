# path='./Logs/repo_commited_in_2023_valid_entry.txt'
path='./Logs/repo_commited_in_2023_100000_valid_entry.txt'
substring="dist"
cat $path | while read rows
do
    if [[ $rows != *"$substring"* ]]; then
        array=(${rows//,/ })
        repo=${array[0]}
        url=${array[1]}
        # echo $repo','$url >> './Logs/repo_commited_in_2023_100000_valid_entry_nodist.txt'
        node ./scripts/extract_module_system.js $repo $url
    fi
done