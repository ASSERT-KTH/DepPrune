#!/bin/bash 

jsonFile='.json'
jsonEmpty='{}'
projectName=$1

# fileName='./Data/'$projectName'/'$projectName'_bloated_pure_deps_variants.txt'
fileName='./Data/'$projectName'/'$projectName'_function_removal.txt'
# fileNameDeps='./Data/'$projectName'/'$projectName'_function_removal.txt'

cat $fileName | while read rows
do
echo $rows
if [ ${rows:0-5} = ${jsonFile} ]
then echo $jsonEmpty > $rows
else node function_remove.js $rows
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
