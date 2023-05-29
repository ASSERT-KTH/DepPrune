path='./Logs/repo_commited_in_2023_valid_entry.txt'
cat $path | while read rows
do
    array=(${rows//,/ })
    repo=${array[0]}
    url=${array[1]}
    node ./scripts/extract_module_system.js $repo $url
done