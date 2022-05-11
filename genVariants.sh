repoUrl=$1
folderPath=$2
entryFile=$3

echo $repoUrl
echo $folderPath
echo $entryFile

rm -rf $folderPath

git clone $repoUrl $folderPath

./resetProject.sh $folderPath

python3 genDepList.py $folderPath "npm install "

python3 genNycRc.py $folderPath "${folderPath}/dep_list.txt"

cd $folderPath

nyc npm run test

cd ../..

./transform.sh $folderPath "dynamic" false

npm install --save dependency-tree

node dep-tree.js $folderPath $entryFile

node traverse-tree.js  $folderPath

# cd ../..



