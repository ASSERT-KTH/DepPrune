#!/bin/bash 

jsonFile='.json'
jsonEmpty='{}'
projectName=$1
strategyName=$2
# file / subtree / pure_deps

fileName='./Data/'$projectName'/'$projectName'_bloated_'$strategyName'_variants.txt'
# fileNameDeps='./Data/'$projectName'/'$projectName'_bloated_deps_variants.txt'

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
