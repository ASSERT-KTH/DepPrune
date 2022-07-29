#!/bin/bash 

jsonFile='.json'
jsonEmpty='{}'
projectName=$1
fileName='./Data/'$1'_bloated_variants.txt'
fileNameDeps='./Data/'$1'_bloated_deps_variants.txt'

cat $fileName | while read rows
do
echo $rows
if [ ${rows:0-5} = ${jsonFile} ]
then echo $jsonEmpty > $rows
else node remove-functions.js $projectName $rows
fi
done

# cat $fileNameDeps | while read rowsDeps
# do
# echo $rowsDeps
# if [ ${rowsDeps:0-5} = ${jsonFile} ]
# then echo $jsonEmpty > $rowsDeps
# else node remove-dep-functions.js $rowsDeps
# fi
# done
