projectName=$1

x=0

# echo "remove direct dep before install"

path='Data/'$projectName'_dependants.log'

cat $path | while read rows
do
echo $rows
node get-package-github-url.js $projectName $rows
done